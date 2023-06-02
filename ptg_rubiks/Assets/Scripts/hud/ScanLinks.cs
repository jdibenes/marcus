
using UnityEngine;

public class ScanLinks : MonoBehaviour, ComponentHUD
{
    const int m_s1_ticks = 30;
    const int m_s2_ticks = 10;
    const int m_s3_ticks = 30;

    uint[,,] m_link_actions =
    {
        { { 6, 0 }, { 7, 1 }, { 8, 2 }, }, // UP -> MX
        { { 0, 6 }, { 1, 7 }, { 2, 8 }, }, // DOWN -> PX
        { { 2, 0 }, { 5, 3 }, { 8, 6 }, }, // LEFT -> MY
        { { 0, 2 }, { 3, 5 }, { 6, 8 }, }, // RIGHT -> PY
    };

    public GameObject[] m_arrow;
    int m_state;
    int m_ticks;    
    int m_direction;
    Vector3[] m_centers;
    ushort m_prev_scan_step;
    bool m_scan_last;

    // Start is called before the first frame update
    void Start()
    {
        m_centers = new Vector3[9];
    }

    // Update is called once per frame
    void Update()
    {
        Vector3 p1;
        Vector3 p2;
        float alpha;

        switch (m_state)
        {
        case 0:
            m_state = 1;
            m_ticks = 0;
            break;
        case 1:
            m_ticks++;
            alpha = m_ticks / (float)m_s1_ticks;
            for (int k = 0; k < 3; ++k)
            {
                p1 = m_centers[m_link_actions[m_direction, k, 0]];
                p2 = m_centers[m_link_actions[m_direction, k, 1]];
                m_arrow[k].GetComponent<Arrow>().SetSpan(p1, (1 - alpha) * p1 + alpha * p2);
            }
            if (m_ticks < m_s1_ticks) { break; }
            m_state = 2;
            m_ticks = 0;
            break;
        case 2:
            m_ticks++;
            if (m_ticks < m_s2_ticks) { break; }
            m_state = 3;
            m_ticks = 0;
            break;
        case 3:
            alpha = m_ticks / (float)m_s3_ticks;
            m_ticks++;
            for (int k = 0; k < 3; ++k)
            {
                p1 = m_centers[m_link_actions[m_direction, k, 0]];
                p2 = m_centers[m_link_actions[m_direction, k, 1]];
                m_arrow[k].GetComponent<Arrow>().SetSpan((1 - alpha) * p1 + alpha * p2, p2);
            }
            if (m_ticks < m_s3_ticks) { break; }
            ResetArrows();
            break;
        }
    }

    void ResetArrows()
    {
        m_state = -1;
        for (int k = 0; k < 3; ++k) { m_arrow[k].transform.localPosition = new Vector3(0, 0, 0); }
    }

    void Fire(int direction, Vector3[] centers)
    {
        m_direction = direction;
        for (int i = 0; i < 9; ++i) { m_centers[i] = new Vector3(centers[i].x, centers[i].y, centers[i].z); }
        m_state = 0;
    }

    public void Draw(ClientStatus client_status)
    {
        if (client_status.top_state != 2) { return; }
        if (m_scan_last && (m_prev_scan_step == 5) && (client_status.step_index == 5) && (client_status.warn_seen != 0) && (client_status.warn_mismatch == 3))
        {
            Fire(0, client_status.centers);
            m_scan_last = false;
        }

        if (m_prev_scan_step == client_status.step_index) { return; }
        switch (client_status.step_index)
        {
        case 0: break;
        case 1:
        case 2:
        case 3:
            Fire(2, client_status.centers);
            break;
        case 4:
            Fire(1, client_status.centers);
            break;
        case 5:
            Fire(0, client_status.centers);
            m_scan_last = true;
            break;
        }
        m_prev_scan_step = client_status.step_index;
    }

    public void Clear()
    {
        m_prev_scan_step = 0xFFFF;
        m_scan_last = false;
        ResetArrows();
    }

    public void Configure(Color arrow_color, float head_factor, float thickness)
    {
        for (int k = 0; k < 3; ++k) { m_arrow[k].GetComponent<Arrow>().SetParameters(arrow_color, head_factor, thickness); }
    }
}
