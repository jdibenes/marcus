
using System;
using UnityEngine;
using Microsoft.MixedReality.Toolkit.Audio;

public class RubiksIPC : MonoBehaviour
{
    ClientStatus m_client_status;

    public GameObject m_contours;
    public GameObject m_reticle;
    public GameObject m_scan_bar;
    public GameObject m_scan_sides;
    public GameObject m_solve_links;
    public GameObject m_scan_links;
    public GameObject m_warning_bar;
    public GameObject m_avatar_portrait;
    public GameObject m_text_slab;
    public GameObject m_text_area;
    public GameObject m_tts;

    void Start()
    {
        m_client_status = new ClientStatus();
        m_client_status.scan_sides = new Color[6];
        m_client_status.centers = new Vector3[9];

        Clear();
    }

    void Update()
    {
        GetMessage();
    }

    void Clear()
    {
        m_contours.GetComponent<Contours>().Clear();
        m_reticle.GetComponent<Reticle>().Clear();
        m_scan_bar.GetComponent<ScanBar>().Clear();
        m_scan_sides.GetComponent<ScanSides>().Clear();
        m_solve_links.GetComponent<SolveLinks>().Clear();
        m_scan_links.GetComponent<ScanLinks>().Clear();
        m_warning_bar.GetComponent<WarningBar>().Clear();
        m_avatar_portrait.GetComponent<AvatarPortrait>().Clear();
        m_text_slab.GetComponent<TextSlab>().Clear();
        m_text_area.GetComponent<TextArea>().Clear();        
    }

    void UnpackStatus(byte[] data)
    {
        m_client_status.top_state = (byte)((data[0] >> 2) & 0x07);
        m_client_status.state = (byte)(data[0] & 0x03);
        m_client_status.detected = (byte)(data[1] & 0x01);
        m_client_status.auto_scan = (byte)((data[1] >> 7) & 0x01);
        m_client_status.step_index = BitConverter.ToUInt16(data, 2);
        m_client_status.step_count = BitConverter.ToUInt16(data, 4);
        m_client_status.action = data[6];
        m_client_status.warn_top = (byte)(data[7] & 3);
        m_client_status.warn_mismatch = (byte)((data[7] >> 2) & 0x7);
        m_client_status.warn_seen = (byte)((data[7] >> 5) & 0x1);
        m_client_status.scale = BitConverter.ToSingle(data, 8);
        m_client_status.progress = BitConverter.ToSingle(data, 12);
        for (int i = 0; i < 6; i++)
        {
            int p = 16 + (i * 4);
            m_client_status.scan_sides[i] = new Color(data[p + 2] / 255.0f, data[p + 1] / 255.0f, data[p] / 255.0f, data[p + 3] / 255.0f);
        }
        if (m_client_status.detected == 0) { return; }
        for (int i = 0; i < 9; ++i)
        {
            int p = 40 + (i * 12);
            m_client_status.centers[i] = transform.InverseTransformPoint(new Vector3(BitConverter.ToSingle(data, p + 0), BitConverter.ToSingle(data, p + 4), BitConverter.ToSingle(data, p + 8)));
        }
    }

    bool GetMessage()
    {
        uint command;
        byte[] data;
        if (!hl2ss.PullMessage(out command, out data)) { return false; }
        hl2ss.PushResult(ProcessMessage(command, data));
        hl2ss.AcknowledgeMessage(command);
        return true;
    }

    uint ProcessMessage(uint command, byte[] data)
    {
        uint ret = 0;

        switch (command)
        {
        case 0:   ret = MSG_Update(data);      break;
        case 1:   ret = MSG_Configure(data);   break;
        case 2:   ret = MSG_SayStep(data);     break;
        case 3:   ret = MSG_SayTop(data);      break;
        case 4:   ret = MSG_TTSBusy(data);     break;
        case 5:   ret = MSG_Acknowledge(data); break;        
        case ~0U: ret = MSG_Disconnect(data);  break;
        }

        return ret;
    }

    uint MSG_Update(byte[] data)
    {
        UnpackStatus(data);
        m_contours.GetComponent<Contours>().Draw(m_client_status);
        m_reticle.GetComponent<Reticle>().Draw(m_client_status);
        m_scan_bar.GetComponent<ScanBar>().Draw(m_client_status);
        m_scan_sides.GetComponent<ScanSides>().Draw(m_client_status);
        m_solve_links.GetComponent<SolveLinks>().Draw(m_client_status);
        m_scan_links.GetComponent<ScanLinks>().Draw(m_client_status);
        m_avatar_portrait.GetComponent<AvatarPortrait>().Draw(m_client_status);
        m_text_slab.GetComponent<TextSlab>().Draw(m_client_status);
        m_text_area.GetComponent<TextArea>().Draw(m_client_status);
        return 1;
    }

    uint MSG_Configure(byte[] data)
    {
        bool show_contours = data[0] != 0;
        Color arrow_color = new Color(data[1] / 255.0f, data[2] / 255.0f, data[3] / 255.0f);
        float head_factor = BitConverter.ToSingle(data, 4);
        float thickness = BitConverter.ToSingle(data, 8);
        float font_size = BitConverter.ToSingle(data, 12);
        Color text_color = new Color(data[16] / 255.0f, data[17] / 255.0f, data[18] / 255.0f);

        m_contours.GetComponent<Contours>().Configure(show_contours);
        m_solve_links.GetComponent<SolveLinks>().Configure(arrow_color, head_factor, thickness);
        m_scan_links.GetComponent<ScanLinks>().Configure(arrow_color, head_factor, thickness);
        m_text_area.GetComponent<TextArea>().Configure(font_size, text_color);
        
        return 1;
    }

    uint MSG_SayStep(byte[] data)
    {
        m_tts.GetComponent<TextToSpeech>().StartSpeaking(GuideScript.BuildStep(m_client_status));
        return 0;
    }

    uint MSG_SayTop(byte[] data)
    {
        m_tts.GetComponent<TextToSpeech>().StartSpeaking(GuideScript.BuildProcess(m_client_status));
        return 0;
    }

    uint MSG_TTSBusy(byte[] data)
    {
        TextToSpeech tts = m_tts.GetComponent<TextToSpeech>();
        return (tts.SpeechTextInQueue() || tts.IsSpeaking()) ? 1U : 0U;
    }

    uint MSG_Acknowledge(byte[] data)
    {
        m_warning_bar.GetComponent<WarningBar>().Draw(m_client_status);
        return 0;
    }

    uint MSG_Disconnect(byte[] data)
    {
        Clear();
        return ~0U;
    }
}
