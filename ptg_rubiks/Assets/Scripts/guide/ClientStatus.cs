
using UnityEngine;

public class ClientStatus
{
    public byte top_state;
    public byte state;
    public byte detected;
    public byte auto_scan;
    public ushort step_index;
    public ushort step_count;
    public byte action;
    public byte warn_top;
    public byte warn_mismatch;
    public byte warn_seen;
    public float scale;
    public float progress;
    public Color[] scan_sides;
    public Vector3[] centers;
}
