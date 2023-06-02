
using UnityEngine;

public class Contours : MonoBehaviour, ComponentHUD
{
    public GameObject[] m_contours;
    bool m_show_contours;

    public void Draw(ClientStatus client_status)
    {
        Clear();
        if (!m_show_contours || (client_status.detected == 0)) { return; }
        for (int i = 0; i < 9; ++i)
        {
            m_contours[i].transform.localPosition = client_status.centers[i];
            m_contours[i].transform.localScale = new Vector3(client_status.scale, client_status.scale, 1);
        }
    }

    public void Clear()
    {
        for (int i = 0; i < 9; ++i) { m_contours[i].transform.localPosition = new Vector3(0, 0, 0); }
    }

    public void Configure(bool show_contours)
    {
        m_show_contours = show_contours;
    }
}
