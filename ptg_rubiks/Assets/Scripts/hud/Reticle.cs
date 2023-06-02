
using UnityEngine;

public class Reticle : MonoBehaviour, ComponentHUD
{
    public Material PMaterial;
    public Material NMaterial;
    public Material XMaterial;

    public void Draw(ClientStatus client_status)
    {
        int i = ((client_status.top_state == 2) || (client_status.top_state == 4)) ? (client_status.detected != 0 ? 1 : 0) : -1;
        Material select;
        switch (i)
        {
        case 0:  select = NMaterial; break;
        case 1:  select = PMaterial; break;
        default: select = XMaterial; break;
        }

        GetComponent<Renderer>().material = select;
    }

    public void Clear()
    {
        GetComponent<Renderer>().material = XMaterial;
    }
}
