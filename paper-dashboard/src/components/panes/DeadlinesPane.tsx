import type { Paper } from '../../types/paper';

function daysUntil(dateStr: string): number {
  const d = new Date(dateStr);
  const now = new Date();
  return Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
}

interface Props {
  paper: Paper;
}

export function DeadlinesPane({ paper }: Props) {
  const allDeadlines = [...paper.deadlines];
  if (paper.progress.revisionDueDate && !allDeadlines.some((d) => d.date === paper.progress.revisionDueDate)) {
    allDeadlines.unshift({
      label: 'Revision due',
      date: paper.progress.revisionDueDate,
      type: 'revision',
    });
  }

  if (allDeadlines.length === 0) {
    return <div style={{ color: '#aaa', fontSize: 12 }}>No upcoming deadlines</div>;
  }

  return (
    <div>
      {allDeadlines
        .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime())
        .map((dl, i) => {
          const days = daysUntil(dl.date);
          const countdownColor = days <= 7 ? '#d04040' : days <= 21 ? '#d09030' : '#40a060';

          return (
            <div
              key={i}
              style={{
                display: 'flex',
                alignItems: 'center',
                padding: '7px 8px',
                borderBottom: '1px solid #f0ede6',
                gap: 10,
                background: i % 2 === 1 ? '#faf8f3' : undefined,
              }}
            >
              <div style={{ minWidth: 50, textAlign: 'center' }}>
                <div style={{ fontSize: 18, fontWeight: 700, color: countdownColor }}>
                  {days < 0 ? 'Past' : days}
                </div>
                <div style={{ fontSize: 9, color: '#888' }}>{days < 0 ? 'due' : 'days'}</div>
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, fontWeight: 600 }}>{dl.label}</div>
                <div style={{ fontSize: 10, color: '#999' }}>
                  {new Date(dl.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              </div>
            </div>
          );
        })}
    </div>
  );
}
