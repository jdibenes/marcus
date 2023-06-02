
using System;

public static class GuideScript
{
    private static string[] m_top = { "white", "blue", "green" };
    private static string[] m_colors = { "white", "red", "green", "yellow", "orange", "blue" };
    private static string[] m_scan_order = { "red", "blue", "orange", "green", "white", "yellow" };

    public static string DefaultCaption = "Waiting for client...<br> <br> ";

    public static string BuildCaption(ClientStatus m_client_status)
    {
        if (m_client_status.top_state == 7) { return "Say HELLO to start!<br> <br> <br> <br> "; }
        if (m_client_status.top_state == 0) { return "Hello, I'm MARCuS.<br>My purpose is to help you solve rubik's cubes.<br>Grab a rubik's cube and settle in.<br>Let me know when you're READY to begin.<br> "; }
        if (m_client_status.top_state == 1) { return "We're going to scan the cube now.<br>Hold the cube so the side with the white center is up<br>and the side with the red center is facing you.<br>Tell me when you're READY!<br> "; }
        if (m_client_status.top_state == 3 && m_client_status.state == 1) { return "Scan complete! Now, we'll solve this cube together.<br>I'll be quiet while you handle the cube but feel free to<br>ask for HELP at any time.<br>Tell me when you're READY!<br> "; }
        if (m_client_status.top_state == 3 && m_client_status.state == 2) { return "This cube is already solved!<br>Say RESET to start over.<br> <br> "; }

        if (m_client_status.state == 2) { return "Well done, you solved the cube!<br>Say RESET to start over.<br> <br> "; } // OK
        if (m_client_status.state == 3) { return "Cube was scanned incorrectly!<br>Say RESET to start over.<br> <br> "; } // OK

        string str_action;

        switch ((uint)m_client_status.action)
        {
        case GuideStatus.ACTION_NONE: // OK
            str_action = "NONE";
            break;
        case GuideStatus.ACTION_WAIT: // OK            
            if (m_client_status.detected == 0)
            {
                str_action = "Show me the cube";
            }
            else if (m_client_status.warn_top == 0)
            {
                str_action = "Analyzing... Keep the cube in view";
            }
            else
            {
                str_action = "Bad orientation";
            }
            break;
        case GuideStatus.ACTION_MOVE_MX: // OK
            str_action = "Rotate the cube away from you";
            break;
        case GuideStatus.ACTION_MOVE_PX: // OK
            str_action = "Rotate the cube towards you";
            break;
        case GuideStatus.ACTION_MOVE_MY: // OK
            str_action = "Rotate the cube to the left";
            break;
        case GuideStatus.ACTION_MOVE_PY: // OK
            str_action = "Rotate the cube to the right";
            break;
        case GuideStatus.ACTION_MOVE_MZ: // OK
            str_action = "Rotate the cube clockwise";
            break;
        case GuideStatus.ACTION_MOVE_PZ: // OK
            str_action = "Rotate the cube counterclockwise";
            break;
        case GuideStatus.ACTION_TURN_MU: // OK
            str_action = "Turn the top layer a quarter turn to the left";
            break;
        case GuideStatus.ACTION_TURN_PU: // OK
            str_action = "Turn the top layer a quarter turn to the right";
            break;
        case GuideStatus.ACTION_TURN_MR: // OK
            str_action = "Turn the right side a quarter turn away from you";
            break;
        case GuideStatus.ACTION_TURN_PR: // OK
            str_action = "Turn the right side a quarter turn towards you";
            break;
        case GuideStatus.ACTION_TURN_MF: // OK
            str_action = "Turn the front side a quarter turn to the right";
            break;
        case GuideStatus.ACTION_TURN_PF: // OK
            str_action = "Turn the front side a quarter turn to the left";
            break;
        case GuideStatus.ACTION_TURN_MD: // OK
            str_action = "Turn the bottom layer a quarter turn to the right";
            break;
        case GuideStatus.ACTION_TURN_PD: // OK
            str_action = "Turn the bottom layer a quarter turn to the left";
            break;
        case GuideStatus.ACTION_TURN_ML: // OK
            str_action = "Turn the left side a quarter turn towards you";
            break;
        case GuideStatus.ACTION_TURN_PL: // OK
            str_action = "Turn the left side a quarter turn away from you";
            break;
        case GuideStatus.ACTION_TURN_MB: // OK
            str_action = "TURN_MB";
            break;
        case GuideStatus.ACTION_TURN_PB: // OK
            str_action = "TURN_PB";
            break;
        case GuideStatus.ACTION_INVALID: // OK
            str_action = "INVALID";
            break;
        case GuideStatus.ACTION_ASK_WHITE: // OK
            str_action = "Show me the side with the white center";
            break;
        case GuideStatus.ACTION_ASK_RED: // OK
            str_action = "Show me the side with the red center";
            break;
        case GuideStatus.ACTION_ASK_GREEN: // OK
            str_action = "Show me the side with the green center";
            break;
        case GuideStatus.ACTION_ASK_YELLOW: // OK
            str_action = "Show me the side with the yellow center";
            break;
        case GuideStatus.ACTION_ASK_ORANGE: // OK
            str_action = "Show me the side with the orange center";
            break;
        case GuideStatus.ACTION_ASK_BLUE: // OK
            str_action = "Show me the side with the blue center";
            break;
        case GuideStatus.ACTION_ASK_RESCAN: // OK
            return "Error detected!<br>Say RESET to start over.<br> <br> ";
        default: // OK
            str_action = string.Format("UNKNOWN ACTION {0}", m_client_status.action);
            break;
        }

        string str_action_modifier = ((m_client_status.state == 0) && (m_client_status.auto_scan == 0)) ? " and tell me to SCAN." : "."; // OK

        string str_warn;
        string str_warn_format = "Make sure the side with the {0} center is up!";

        switch (m_client_status.warn_top)
        {
        case 0: // OK
            str_warn = "";
            break;
        case 1: // OK
        case 2: // OK
        case 3: // OK
            str_warn = string.Format(str_warn_format, m_top[m_client_status.warn_top - 1]);
            break;
        default: // OK
            str_warn = string.Format("UNKNOWN WARN {0}", m_client_status.warn_top);
            break;
        }

        string str_warn_scan;
        string str_warn_scan_format = m_client_status.warn_seen == 0 ? "The center looks {0}. Do you want to SCAN anyway?" : "I've scanned the {0} side.";

        switch (m_client_status.warn_mismatch)
        {
        case 0: // OK
            str_warn_scan = m_client_status.warn_seen == 0 ? "" : "UNKNOWN WARN_SEEN 0";
            break;
        case 1: // OK
        case 2: // OK
        case 3: // OK
        case 4: // OK
        case 5: // OK
        case 6: // OK
            str_warn_scan = string.Format(str_warn_scan_format, m_colors[m_client_status.warn_mismatch - 1]);
            break;
        default: // OK
            str_warn_scan = string.Format("UNKNOWN WARN_MISMATCH {0}", m_client_status.warn_mismatch);
            break;
        }

        if (m_client_status.detected == 0) { str_warn_scan = ""; } // OK

        string str_step = (m_client_status.state == 1) ? string.Format("Steps completed: {0} of {1}.", m_client_status.step_index, m_client_status.step_count) : ""; // OK

        return str_warn_scan + "<br>" + str_action + str_action_modifier + "<br>" + str_warn + "<br>" + str_step + "<br> "; // OK
    }

    public static string BuildStep(ClientStatus m_client_status)
    {
        string step_string = BuildCaption(m_client_status);
        string[] steps = step_string.Split(new[] { "<br>" }, StringSplitOptions.None);

        if (m_client_status.top_state == 7) { return steps[0]; }
        if (m_client_status.top_state == 0) { return steps[0] + " " + steps[1] + " " + steps[2] + " " + steps[3]; }
        if (m_client_status.top_state == 1) { return steps[0] + " " + steps[1] + " " + steps[2] + " " + steps[3]; }
        if (m_client_status.top_state == 3 && m_client_status.state == 1) { return steps[0] + " " + steps[1] + " " + steps[2] + " " + steps[3]; }
        if (m_client_status.top_state == 3 && m_client_status.state == 2) { return steps[0] + " " + steps[1]; }

        if (m_client_status.state == 2 || m_client_status.state == 3 || m_client_status.action == GuideStatus.ACTION_ASK_RESCAN) { return steps[0] + " " + steps[1]; }

        if (m_client_status.state == 0)
        {
            if (m_client_status.warn_seen != 0) { return steps[1] + " " + steps[2]; }
            if (m_client_status.detected == 0) { return steps[1] + " " + steps[2]; }

            switch (m_client_status.warn_mismatch)
            {
            case 0x0:
                return steps[1] + " " + steps[2];
            case 0x1:
            case 0x2:
            case 0x3:
            case 0x4:
            case 0x5:
            case 0x6:
                return "I asked you to show me the " + m_scan_order[m_client_status.step_index] + " side, but this side looks " + m_colors[m_client_status.warn_mismatch - 1] + ". Do you want me to SCAN anyway?";
            }

            return "";
        }

        int option = (string.IsNullOrWhiteSpace(steps[1]) ? 2 : 0) | (string.IsNullOrWhiteSpace(steps[2]) ? 1 : 0);

        switch (option)
        {
        case 0:
            return steps[1] + " " + steps[2];
        case 1:
            return steps[1];
        case 2:
            return steps[2];
        }

        return "";
    }

    public static string BuildProcess(ClientStatus client_status)
    {
        if (client_status.top_state == 7) { return "Hello."; }
        if (client_status.top_state == 0) { return "I'm waiting for you to get a rubik's cube before we begin. Tell me when you're ready."; }
        if (client_status.top_state == 1) { return "We're getting ready to scan the cube. Tell me when you're ready."; }
        if (client_status.top_state == 2) { return "I'm scanning the cube with your help. I need to scan it to find the solution and help you solve it."; }
        if (client_status.top_state == 3)
        {
            if (client_status.state == 1) { return "We just finished scanning the cube and are going to solve it now. Tell me when you're ready."; }
            if (client_status.state == 2) { return "We just finished scanning the cube. The cube is already solved. Say reset if you wish to solve another cube."; }
            if (client_status.state == 3) { return "We just finished scanning the cube. The cube was scanned incorrectly, unfortunately. For best results, please follow the instructions on screen carefully next time. Say reset to try again!"; }
        }
        if (client_status.top_state == 4) { return "You're solving the cube with my help... hopefully. Follow the instructions on screen carefully."; }
        if (client_status.top_state == 5) { return "The cube has been solved. Say reset if you wish to solve another cube."; }
        return "";
    }
}
