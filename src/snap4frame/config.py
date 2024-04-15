from snap4frame.types import Parameters

FRAME_DECODER = Parameters(
    {
        "cwd_replace": "${CWD}",
    }
)

TRACEBACK_TYPE_DECODER = Parameters(
    {
        "exclude_frames": [],
        "include_frames": [],
    }
)
