
using UnityEngine;

public class SolveLinks : MonoBehaviour, ComponentHUD
{
    uint[,,,] m_link_actions;

    public GameObject[] m_arrow;

    public void Start()
    {
        m_link_actions = new uint[2, 9, 4, 3];

        uint[] z1 = { 6, 0, 7, 4 };
        uint[] z2 = { 0, 2, 4, 5 };

        uint[] f1 = { 1, 5, 7, 3 };
        uint[] f2 = { 5, 7, 3, 1 };

        for (uint i = 0; i < 3; ++i) { m_link_actions[0, 0, i, 0] = 1; m_link_actions[0, 0, i, 1] = i + 6; m_link_actions[0, 0, i, 2] = i; }
        for (uint i = 0; i < 3; ++i) { m_link_actions[0, 1, i, 0] = 1; m_link_actions[0, 1, i, 1] = 3 * i + 2; m_link_actions[0, 1, i, 2] = 3 * i; }
        for (uint i = 0; i < 4; ++i) { m_link_actions[0, 2, i, 0] = 1; m_link_actions[0, 2, i, 1] = z1[i]; m_link_actions[0, 2, i, 2] = z2[i]; }
        for (uint i = 0; i < 1; ++i) { m_link_actions[0, 3, i, 0] = 1; m_link_actions[0, 3, i, 1] = 2; m_link_actions[0, 3, i, 2] = 0; }
        for (uint i = 0; i < 1; ++i) { m_link_actions[0, 4, i, 0] = 1; m_link_actions[0, 4, i, 1] = 8; m_link_actions[0, 4, i, 2] = 2; }
        for (uint i = 0; i < 4; ++i) { m_link_actions[0, 5, i, 0] = 1; m_link_actions[0, 5, i, 1] = f1[i]; m_link_actions[0, 5, i, 2] = f2[i]; }
        for (uint i = 0; i < 1; ++i) { m_link_actions[0, 6, i, 0] = 1; m_link_actions[0, 6, i, 1] = 6; m_link_actions[0, 6, i, 2] = 8; }
        for (uint i = 0; i < 1; ++i) { m_link_actions[0, 7, i, 0] = 1; m_link_actions[0, 7, i, 1] = 0; m_link_actions[0, 7, i, 2] = 6; }
        for (uint i = 0; i < 2; ++i) { m_link_actions[0, 8, i, 0] = 1; m_link_actions[0, 8, i, 1] = 8 - 2 * i; m_link_actions[0, 8, i, 2] = 2 * i; }

        for (uint i = 0; i < 9; ++i)
        {
            for (uint j = 0; j < 4; ++j)
            {
                m_link_actions[1, i, j, 0] = m_link_actions[0, i, j, 0];
                m_link_actions[1, i, j, 1] = m_link_actions[0, i, j, 2];
                m_link_actions[1, i, j, 2] = m_link_actions[0, i, j, 1];
            }
        }
    }

    public void Draw(ClientStatus client_status)
    {
        uint i;

        Clear();
        if (client_status.top_state != 4) { return; }
        if (client_status.detected == 0) { return; }

        switch (client_status.action & ~GuideStatus.ACTION_P)
        {
        case GuideStatus.ACTION_MOVE_MX: i = 0; break;
        case GuideStatus.ACTION_MOVE_MY: i = 1; break;
        case GuideStatus.ACTION_MOVE_MZ: i = 2; break;
        case GuideStatus.ACTION_TURN_MU: i = 3; break;
        case GuideStatus.ACTION_TURN_MR: i = 4; break;
        case GuideStatus.ACTION_TURN_MF: i = 5; break;
        case GuideStatus.ACTION_TURN_MD: i = 6; break;
        case GuideStatus.ACTION_TURN_ML: i = 7; break;
        case GuideStatus.ACTION_TURN_MB: i = 8; break;
        default: return;
        }

        uint p = client_status.action & GuideStatus.ACTION_P;

        for (int k = 0; k < 4; ++k)
        {
            if (m_link_actions[p, i, k, 0] != 0)
            {
                m_arrow[k].GetComponent<Arrow>().SetSpan(client_status.centers[m_link_actions[p, i, k, 1]], client_status.centers[m_link_actions[p, i, k, 2]]);
            }
        }
    }

    public void Clear()
    {
        for (int k = 0; k < 4; ++k) { m_arrow[k].transform.localPosition = new Vector3(0, 0, 0); }
    }

    public void Configure(Color arrow_color, float head_factor, float thickness)
    {
        for (int k = 0; k < 4; ++k) { m_arrow[k].GetComponent<Arrow>().SetParameters(arrow_color, head_factor, thickness); }
    }
}
