import datetime as dt
import importlib_resources
import json
import warnings

import matplotlib.pyplot as plt
import numpy as np
import spiceypy as spice

from uvisaurorae.data_retrieval import download_data
from uvisaurorae.inout import load_integrated_data, save_to_fits
from uvisaurorae.plotting import plot_auroral_image
from uvisaurorae.projection import project_data, project_data_parallel


class CommandError(Exception):
    def __init__(self, msg=None):
        super(CommandError, self).__init__(msg)


def get_full_execution_list():
    execution_list_file = importlib_resources.files("uvisaurorae.resources").joinpath(
        "full_command_list.json"
    )
    with open(execution_list_file, "r") as f:
        execution_list = json.loads(f.read())
    return execution_list


def execute_projection_command(cmd_dict):
    projection_mode = cmd_dict.pop("projection_mode", None)
    if projection_mode is None:
        raise CommandError("No projection mode given")
    elif projection_mode == "split":
        cmd_dict.pop("clean", None)
        split_files(**cmd_dict)
    elif projection_mode == "combine":
        cmd_dict.pop("only_idx", None)
        combine_files(**cmd_dict)
    else:
        raise CommandError("Invalid projection mode given")


def split_files(
    uvis_file_names,
    release_number,
    uvis_dir,
    spice_dir,
    uvis_projector,
    projection_dir,
    sensitivity=1,
    creator="unknown",
    n_workers=None,
    overwrite=False,
    compress=True,
    only_idx=None,
):

    files = [
        download_data(
            n,
            release_number,
            uvis_dir,
            spice_dir,
            overwrite=overwrite,
            compress=compress,
        )
        for n in uvis_file_names
    ]

    proj_func = project_data if n_workers == 1 else project_data_parallel

    metadata = None
    et_times = None
    int_data = None
    for file in files:
        lbl_suffix = ".LBL" if ".DAT" in str(file) else ".lbl"
        tmp_metadata, tmp_et_times, tmp_int_data = load_integrated_data(
            file, str(file).split(".DAT")[0] + lbl_suffix
        )
        if metadata is None:
            metadata = tmp_metadata
            et_times = tmp_et_times
            int_data = tmp_int_data
        else:
            for item in [
                "LINE_BIN",
                "UL_CORNER_LINE",
                "LR_CORNER_LINE",
                "INTEGRATION_DURATION",
            ]:
                if metadata[item] != tmp_metadata[item]:
                    raise CommandError(
                        f"Cannot combine-split {uvis_file_names}, different observation parameters"
                    )
            metadata["FILE_RECORDS"] += tmp_metadata["FILE_RECORDS"]
            metadata["STOP_TIME"] = tmp_metadata["STOP_TIME"]

            et_times = np.append(et_times, tmp_et_times, axis=0)
            int_data = np.append(int_data, tmp_int_data, axis=0)

    uvis_projector.reset_spice()

    min_list, max_list = get_split_limits(et_times, sensitivity=sensitivity)

    if only_idx is not None:
        min_list = min_list[only_idx]
        max_list = max_list[only_idx]

    for rec_start, rec_stop in zip(min_list, max_list):
        save_metadata = dict()
        save_metadata["START_TIME"] = metadata["START_TIME"] + dt.timedelta(
            seconds=rec_start * metadata["INTEGRATION_DURATION"]
        )
        save_metadata["STOP_TIME"] = metadata["START_TIME"] + dt.timedelta(
            seconds=(rec_stop + 1) * metadata["INTEGRATION_DURATION"]
        )
        save_metadata["TOTAL_EXPOSURE"] = (rec_stop - rec_start) * metadata[
            "INTEGRATION_DURATION"
        ]
        save_metadata["FILE_RECORDS"] = rec_stop - rec_start

        kwargs = dict(records=np.arange(rec_start, rec_stop + 1))
        if n_workers != 1:
            kwargs.update(n_workers=n_workers)

        proj_sum, proj_num, proj_min_angle = proj_func(
            uvis_projector,
            int_data,
            et_times,
            metadata["LINE_BIN"],
            metadata["UL_CORNER_LINE"],
            metadata["LR_CORNER_LINE"],
            **kwargs,
        )

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            projection = proj_sum / proj_num

        file_name, hemisphere = save_to_fits(
            projection_dir,
            projection,
            proj_min_angle,
            creator,
            save_metadata,
        )

        plot_auroral_image(projection, hemisphere=hemisphere)
        plot_dir = file_name.parent / "previews"
        if not plot_dir.exists():
            plot_dir.mkdir(parents=True)
        plt.savefig(plot_dir / (file_name.stem + ".png"), bbox_inches="tight", dpi=300)
        plt.close()


def combine_files(
    uvis_file_names,
    release_number,
    uvis_dir,
    spice_dir,
    uvis_projector,
    projection_dir,
    sensitivity=5,
    creator="unknown",
    n_workers=None,
    overwrite=False,
    compress=True,
    clean=True,
):
    file_list = [
        download_data(
            n,
            release_number,
            uvis_dir,
            spice_dir,
            overwrite=overwrite,
            compress=compress,
        )
        for n in uvis_file_names
    ]

    proj_func = project_data if n_workers == 1 else project_data_parallel

    uvis_projector.reset_spice()

    save_metadata = dict()
    save_metadata["START_TIME"] = dt.datetime.now()
    save_metadata["STOP_TIME"] = dt.datetime.now()
    save_metadata["TOTAL_EXPOSURE"] = 0
    save_metadata["FILE_RECORDS"] = 0

    all_proj_sum = []
    all_proj_num = []
    all_proj_min_angle = []

    for f in file_list:
        lbl_suffix = ".LBL" if ".DAT" in str(f) else ".lbl"
        metadata, et_times, int_data = load_integrated_data(
            f, str(f).split(".DAT")[0] + lbl_suffix
        )

        if clean:
            min_list, max_list = get_split_limits(et_times, sensitivity=sensitivity)
            use_records = np.concatenate(
                [np.arange(min_list[i], max_list[i]) for i in range(len(min_list))]
            )
            use_records = np.unique(use_records)
        else:
            use_records = np.arange(len(et_times))

        if metadata["START_TIME"] < save_metadata["START_TIME"]:
            save_metadata["START_TIME"] = metadata["START_TIME"]
        if metadata["STOP_TIME"] > save_metadata["STOP_TIME"]:
            save_metadata["STOP_TIME"] = metadata["STOP_TIME"]
        save_metadata["TOTAL_EXPOSURE"] += metadata["INTEGRATION_DURATION"] * len(
            use_records
        )
        save_metadata["FILE_RECORDS"] += len(use_records)

        kwargs = dict(records=use_records)
        if n_workers != 1:
            kwargs.update(n_workers=n_workers)

        proj_sum, proj_num, proj_min_angle = proj_func(
            uvis_projector,
            int_data,
            et_times,
            metadata["LINE_BIN"],
            metadata["UL_CORNER_LINE"],
            metadata["LR_CORNER_LINE"],
            **kwargs,
        )

        all_proj_sum.append(proj_sum)
        all_proj_num.append(proj_num)
        all_proj_min_angle.append(proj_min_angle)

    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        all_proj_sum = np.nansum(all_proj_sum, axis=0)
        all_proj_num = np.nansum(all_proj_num, axis=0)
        all_proj_min_angle = np.nanmin(all_proj_min_angle, axis=0)
        all_proj_min_angle[all_proj_num == 0] = np.nan
        projection = all_proj_sum / all_proj_num

    file_name, hemisphere = save_to_fits(
        projection_dir,
        projection,
        all_proj_min_angle,
        creator,
        save_metadata,
    )

    plot_auroral_image(projection, hemisphere=hemisphere)
    plot_dir = file_name.parent / "previews"
    if not plot_dir.exists():
        plot_dir.mkdir(parents=True)
    plt.savefig(plot_dir / (file_name.stem + ".png"), bbox_inches="tight", dpi=300)
    plt.close()


def get_split_limits(et_times, sensitivity=1):
    # Get UVIS boresight in KSM coordinates
    boresight = np.array([0, 0, 1])
    boresight_ksm = np.full((len(et_times), 3), np.nan)
    for iii in range(len(et_times)):
        boresight_ksm[iii, :] = np.matmul(
            spice.pxform("CASSINI_UVIS_FUV", "CASSINI_KSMAG", et_times[iii]),
            boresight,
        )

    # Angular difference between boresight at each timestep
    angle_diff = np.array(
        [
            np.abs(np.arccos(np.dot(boresight_ksm[iii], boresight_ksm[iii + 1])))
            for iii in range(len(boresight_ksm) - 1)
        ]
    )

    # Gradient of angular difference
    diff_grad = np.abs(np.gradient(angle_diff))
    # Find where the gradient is high (boresight angle change is accelerated compared to the mean)
    ind = np.where(diff_grad > np.nanmean(diff_grad) * sensitivity)[0]
    ind = np.unique(np.concatenate([[0], ind, [len(et_times) - 2]]))
    # Find first period with reasonably long constant change in angle and calculate average rotation rate in this period
    tmp = np.where(np.diff(ind) > np.nanmean(np.diff(ind)[np.diff(ind) > 1]) / 2)[0]
    avg_diff = np.nanmean(np.abs(angle_diff[ind[tmp[0]] : ind[tmp[0] + 1]]))

    # Go through list of indices with increased angular change
    minlist = np.array([])
    maxlist = np.array([])
    for iii in range(len(ind) - 1):
        this_idx, next_idx = ind[iii : iii + 2]
        this_angle_diff = np.nanmean(angle_diff[this_idx:next_idx])
        # Discard short periods (aka scans while the s/c was rotating back to start position)
        if (next_idx - this_idx) < 5:
            continue
        # Discard scans with higher and lower rotation rates
        if this_angle_diff > 1.25 * avg_diff * sensitivity:
            continue
        if this_angle_diff < 0.8 * avg_diff / sensitivity:
            continue
        minlist = np.append(minlist, this_idx)
        maxlist = np.append(maxlist, min(next_idx + 1, len(et_times) - 2))
    return minlist, maxlist
