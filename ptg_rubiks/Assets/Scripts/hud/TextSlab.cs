
using UnityEngine;

public class TextSlab : MonoBehaviour, ComponentHUD
{
    Color m_color_blue = new Color(0.0f, 0.0f, 64.0f / 255.0f, 1.0f);
    Color m_color_yellow = new Color(96.0f / 255.0f, 96.0f / 255.0f, 0.0f, 1.0f);
    Color m_color_green = new Color(0.0f, 96.0f / 255.0f, 0.0f, 1.0f);
    Color m_color_red = new Color(128.0f / 255.0f, 0.0f, 0.0f, 1.0f);
    Color m_color_orange = new Color(128.0f / 255.0f, 64.0f / 255.0f, 0.0f, 1.0f);

    public void Draw(ClientStatus m_client_status)
    {
        Color color = m_color_blue;
        switch (m_client_status.top_state)
        {
        case 2:
            if ((m_client_status.warn_mismatch != 0) || (m_client_status.warn_seen != 0)) { color = m_color_yellow; }
            break;
        case 3:
            switch (m_client_status.state)
            {
            case 2: color = m_color_green; break;
            case 3: color = m_color_red; break;
            }
            break;
        case 4:
            if (m_client_status.warn_top != 0) { color = m_color_yellow; }

            switch ((uint)m_client_status.action)
            {
            case GuideStatus.ACTION_NONE: color = m_color_green; break;
            case GuideStatus.ACTION_WAIT: color = m_color_orange; break;
            case GuideStatus.ACTION_ASK_RESCAN: color = m_color_red; break;
            case GuideStatus.ACTION_ASK_WHITE:
            case GuideStatus.ACTION_ASK_RED:
            case GuideStatus.ACTION_ASK_GREEN:
            case GuideStatus.ACTION_ASK_YELLOW:
            case GuideStatus.ACTION_ASK_ORANGE:
            case GuideStatus.ACTION_ASK_BLUE: color = m_color_yellow; break;
            }
            break;
        case 5:
            color = m_color_green;
            break;
        }

        GetComponent<Renderer>().material.color = color;
    }

    public void Clear()
    {
        GetComponent<Renderer>().material.color = m_color_blue;
    }
}
