
using UnityEngine;

public class ScanBar : MonoBehaviour, ComponentHUD
{
    public void Draw(ClientStatus client_status)
    {
        float progress = ((client_status.top_state == 2) || (client_status.top_state == 4)) ? client_status.progress : 0.0f;
        Vector3 scale = transform.localScale;
        Vector3 pos = transform.localPosition;
        scale.x = progress * 0.058f;
        pos.x = -0.029f + (scale.x / 2.0f);
        transform.localScale = scale;
        transform.localPosition = pos;
    }

    public void Clear()
    {
        Vector3 scale = transform.localScale;
        scale.x = 0;
        transform.localScale = scale;
    }
}
