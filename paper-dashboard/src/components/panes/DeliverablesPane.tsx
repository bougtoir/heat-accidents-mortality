import type { Paper } from '../../types/paper';

const TYPE_ICONS: Record<string, string> = {
  manuscript: '\uD83D\uDCC4',
  figure: '\uD83D\uDCCA',
  table: '\uD83D\uDCC8',
  supplement: '\uD83D\uDCCE',
  'cover-letter': '\u2709',
  response: '\uD83D\uDCC4',
  other: '\uD83D\uDCC1',
};

const STATUS_STYLES: Record<string, { color: string; label: string }> = {
  complete: { color: '#40a060', label: 'Complete' },
  'in-progress': { color: '#e0a040', label: 'In Progress' },
  pending: { color: '#bbb', label: 'Pending' },
};

interface Props {
  paper: Paper;
}

export function DeliverablesPane({ paper }: Props) {
  if (paper.deliverables.length === 0) {
    return <div style={{ color: '#aaa', fontSize: 12 }}>No deliverables</div>;
  }

  return (
    <div>
      {paper.deliverables.map((d, i) => {
        const st = STATUS_STYLES[d.status] ?? STATUS_STYLES.pending;
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              padding: '6px 8px',
              borderBottom: '1px solid #f0ede6',
              gap: 8,
              background: i % 2 === 1 ? '#faf8f3' : undefined,
            }}
          >
            <span style={{ fontSize: 16 }}>{TYPE_ICONS[d.type] ?? TYPE_ICONS.other}</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, fontWeight: 600 }}>{d.name}</div>
              <div style={{ fontSize: 10, color: '#999' }}>
                {d.version && `${d.version} \u2022 `}
                {d.lastUpdated ?? 'Not started'}
              </div>
            </div>
            <div style={{ fontSize: 10, color: st.color, fontWeight: 600 }}>{st.label}</div>
          </div>
        );
      })}
    </div>
  );
}
