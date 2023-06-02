
public static class GuideStatus
{
    public const uint ACTION_NONE = 0;
    public const uint ACTION_P    = 1;

    public const uint ACTION_MOVE_MX =  2;
    public const uint ACTION_MOVE_MY =  4;
    public const uint ACTION_MOVE_MZ =  6;
    public const uint ACTION_TURN_MU =  8;
    public const uint ACTION_TURN_MR = 10;
    public const uint ACTION_TURN_MF = 12;
    public const uint ACTION_TURN_MD = 14;
    public const uint ACTION_TURN_ML = 16;
    public const uint ACTION_TURN_MB = 18;

    public const uint ACTION_WAIT    = ACTION_NONE    | ACTION_P;
    public const uint ACTION_MOVE_PX = ACTION_MOVE_MX | ACTION_P;
    public const uint ACTION_MOVE_PY = ACTION_MOVE_MY | ACTION_P;
    public const uint ACTION_MOVE_PZ = ACTION_MOVE_MZ | ACTION_P;
    public const uint ACTION_TURN_PU = ACTION_TURN_MU | ACTION_P;
    public const uint ACTION_TURN_PR = ACTION_TURN_MR | ACTION_P;
    public const uint ACTION_TURN_PF = ACTION_TURN_MF | ACTION_P;
    public const uint ACTION_TURN_PD = ACTION_TURN_MD | ACTION_P;
    public const uint ACTION_TURN_PL = ACTION_TURN_ML | ACTION_P;
    public const uint ACTION_TURN_PB = ACTION_TURN_MB | ACTION_P;

    public const uint ACTION_INVALID = 31;

    public const uint ACTION_ASK_WHITE  = 32;
    public const uint ACTION_ASK_RED    = 33;
    public const uint ACTION_ASK_GREEN  = 34;
    public const uint ACTION_ASK_YELLOW = 35;
    public const uint ACTION_ASK_ORANGE = 36;
    public const uint ACTION_ASK_BLUE   = 37;

    public const uint ACTION_ASK_RESCAN = 63;

    public const uint ERROR_LOST_STATE         = 64;
    public const uint ERROR_INCONSISTENT_STATE = 65;

    public const uint WARN_NONE = 0;

    public const uint WARN_TOP_WHITE = 1;
    public const uint WARN_TOP_BLUE  = 2;
    public const uint WARN_TOP_GREEN = 3;

    public const uint WARN_MISMATCH_WHITE  = 1 << 2;
    public const uint WARN_MISMATCH_RED    = 2 << 2;
    public const uint WARN_MISMATCH_GREEN  = 3 << 2;
    public const uint WARN_MISMATCH_YELLOW = 4 << 2;
    public const uint WARN_MISMATCH_ORANGE = 5 << 2;
    public const uint WARN_MISMATCH_BLUE   = 6 << 2;

    public const uint WARN_SEEN_WHITE  =  9 << 2;
    public const uint WARN_SEEN_RED    = 10 << 2;
    public const uint WARN_SEEN_GREEN  = 11 << 2;
    public const uint WARN_SEEN_YELLOW = 12 << 2;
    public const uint WARN_SEEN_ORANGE = 13 << 2;
    public const uint WARN_SEEN_BLUE   = 14 << 2;
}
