using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ScanSides : MonoBehaviour, ComponentHUD
{
    public void Draw(ClientStatus client_status)
    {
        transform.Find("red").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[0] : Color.clear;
        transform.Find("blue").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[1] : Color.clear;
        transform.Find("orange").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[2] : Color.clear;
        transform.Find("green").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[3] : Color.clear;
        transform.Find("white").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[4] : Color.clear;
        transform.Find("yellow").gameObject.GetComponent<Renderer>().material.color = client_status.top_state == 2 ? client_status.scan_sides[5] : Color.clear;
    }

    public void Clear()
    {
        transform.Find("red").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
        transform.Find("blue").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
        transform.Find("orange").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
        transform.Find("green").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
        transform.Find("white").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
        transform.Find("yellow").gameObject.GetComponent<Renderer>().material.color = new Color(0, 0, 0, 0);
    }
}
