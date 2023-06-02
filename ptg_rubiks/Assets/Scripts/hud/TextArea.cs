
using UnityEngine;
using TMPro;

public class TextArea : MonoBehaviour, ComponentHUD
{
    public void Draw(ClientStatus client_status)
    {
        GetComponent<TextMeshPro>().text = GuideScript.BuildCaption(client_status);
    }

    public void Clear()
    {
        GetComponent<TextMeshPro>().text = GuideScript.DefaultCaption;
    }

    public void Configure(float font_size, Color text_color)
    {
        TextMeshPro tmp = GetComponent<TextMeshPro>();
        tmp.fontSize = font_size;
        tmp.color = text_color;
    }
}
