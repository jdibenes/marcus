
using UnityEngine;

public class AvatarPortrait : MonoBehaviour, ComponentHUD
{
    public Material m_intro;
    public Material m_prescan;
    public Material m_already;
    public Material m_badscan;
    public Material m_presolve;
    public Material m_solved;
    public Material m_hidden;

    public void Draw(ClientStatus client_status)
    {
        int state;
        switch (client_status.top_state)
        {
        case 0: state = 0; break;
        case 1: state = 1; break;
        case 3:
            switch (client_status.state)
            {
            case 1: state = 4; break;
            case 2: state = 2; break;
            case 3: state = 3; break;
            default: state = -1; break;
            }
            break;
        case 5: state = 5; break;
        default: state = -1; break;
        }

        Material select;

        switch (state)
        {
        case 0:  select = m_intro;    break;
        case 1:  select = m_prescan;  break;
        case 2:  select = m_already;  break;
        case 3:  select = m_badscan;  break;
        case 4:  select = m_presolve; break;
        case 5:  select = m_solved;   break;
        default: select = m_hidden;   break;
        }

        gameObject.GetComponent<Renderer>().material = select;
    }

    public void Clear()
    {
        gameObject.GetComponent<Renderer>().material = m_hidden;
    }
}
