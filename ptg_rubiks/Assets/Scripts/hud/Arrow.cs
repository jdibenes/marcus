
using UnityEngine;

public class Arrow : MonoBehaviour
{
    GameObject m_line;
    GameObject m_up;
    GameObject m_down;

    float m_head_factor;
    float m_thickness;

    // Start is called before the first frame update
    void Start()
    {
        m_line = transform.Find("line").gameObject;
        m_up = transform.Find("up").gameObject;
        m_down = transform.Find("down").gameObject;

        SetParameters(Color.magenta, 1.0f / 5.0f, 0.003f);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetParameters(Color color, float head_factor, float thickness)
    {
        m_line.GetComponent<Renderer>().material.color = color;
        m_up.GetComponent<Renderer>().material.color = color;
        m_down.GetComponent<Renderer>().material.color = color;

        m_head_factor = head_factor;
        m_thickness = thickness;
    }

    public void SetSpan(Vector3 p1, Vector3 p2)
    {
        Vector3 center = (p1 + p2) / 2;
        Vector3 dp = p2 - p1;
        float sqrt2 = Mathf.Sqrt(2);
        float L = dp.magnitude;
        float l = m_head_factor * L;
        float y = 1 / (2 * sqrt2) * Mathf.Abs(m_thickness - l);
        float x = (L + (1 - sqrt2) * m_thickness) / 2 - y;

        m_line.transform.localScale = new Vector3(L, m_thickness, 1);
        m_up.transform.localScale = new Vector3(l, m_thickness, 1);
        m_down.transform.localScale = new Vector3(l, m_thickness, 1);

        m_up.transform.localPosition = new Vector3(x, y, 0);
        m_up.transform.localEulerAngles = new Vector3(0, 0, -45);
        m_down.transform.localPosition = new Vector3(x, -y, 0);        
        m_down.transform.localEulerAngles = new Vector3(0, 0, 45);

        gameObject.transform.localPosition = center;
        gameObject.transform.localEulerAngles = new Vector3(0, 0, Mathf.Rad2Deg * Mathf.Atan2(dp.y, dp.x));
    }
}
