
using UnityEngine;

public class WarningBar : MonoBehaviour, ComponentHUD
{
    const int m_s1_ticks = 5;
    const int m_s2_ticks = 30;
    const int m_s3_ticks = 30;
    const int m_s4_ticks = 30;

    int m_state;
    int m_ticks;

    Vector3 m_start_scale;
    Vector3 m_end_scale;
    Vector3 m_start_position;
    Vector3 m_end_position;

    // Update is called once per frame
    void Update()
    {
        float alpha;
        float z;
        Vector3 pos;
        Vector3 scale;

        switch (m_state)
        {
        case 0:
            transform.localScale = new Vector3(0.058f, 0.0185f, 1.0f);
            transform.localPosition = new Vector3(0.0f, -0.03175f, 0.0f);
            m_state = 1;
            m_ticks = 0;
            break;
        case 1:
            z = (m_ticks % (2 * m_s1_ticks)) < m_s1_ticks ? 0.0f : 0.199f;
            pos = transform.localPosition;
            pos.z = z;
            transform.localPosition = pos;
            m_ticks++;
            if (m_ticks < 4*m_s1_ticks) { break; }
            m_state = 2;
            m_ticks = 0;
            break;
        case 2:
            m_ticks++;
            if (m_ticks < m_s2_ticks) { break; }
            m_state = 3;
            m_ticks = 0;
            m_start_scale = transform.localScale;
            m_end_scale = new Vector3(0.058f, 0.002f, 1.0f);
            break;
        case 3:
            alpha = m_ticks / (float)m_s3_ticks;
            m_ticks++;
            transform.localScale = (1 - alpha) * m_start_scale + alpha * m_end_scale;
            pos = transform.localPosition;
            pos.y = (1 - alpha) * -0.03175f + alpha * -0.04f;
            transform.localPosition = pos;
            if (m_ticks < m_s3_ticks) { break; }
            m_state = 4;
            m_ticks = 0;
            m_start_position = transform.localPosition;
            m_end_position = new Vector3(0.0f, -0.11f, 0.501f);
            break;
        case 4:
            alpha = m_ticks / (float)m_s4_ticks;
            m_ticks++;
            transform.localPosition = (1 - alpha) * m_start_position + alpha * m_end_position;
            scale = transform.localScale;
            scale.x = (1 - alpha) * 0.058f + alpha * 0.25f;
            transform.localScale = scale;
            if (m_ticks < m_s4_ticks) { break; }
            Clear();
            break;
        }
    }

    public void Draw(ClientStatus client_status)
    {
        m_state = 0;
    }

    public void Clear()
    {
        m_state = -1;
        transform.localPosition = new Vector3(0, 0, 0);
    }
}
