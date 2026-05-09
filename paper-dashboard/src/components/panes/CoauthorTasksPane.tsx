import type { Paper } from '../../types/paper';

const TASK_STATUS: Record<string, { bg: string; color: string; label: string }> = {
  done: { bg: '#e0f0e8', color: '#408060', label: 'Done' },
  'in-progress': { bg: '#fdf0d0', color: '#a07020', label: 'In Progress' },
  waiting: { bg: '#fde0e0', color: '#c04040', label: 'Waiting' },
};

interface Props {
  paper: Paper;
}

export function CoauthorTasksPane({ paper }: Props) {
  if (paper.coauthorTasks.length === 0) {
    return <div style={{ color: '#aaa', fontSize: 12 }}>No tasks assigned</div>;
  }

  return (
    <div>
      {paper.coauthorTasks.map((ct, i) => {
        const ts = TASK_STATUS[ct.status] ?? TASK_STATUS['in-progress'];
        return (
          <div
            key={i}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 8,
              padding: '6px 8px',
              borderBottom: '1px solid #f0ede6',
              background: i % 2 === 1 ? '#faf8f3' : undefined,
            }}
          >
            <div
              style={{
                width: 28,
                height: 28,
                borderRadius: '50%',
                background: ct.color ?? '#2a7a8a',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 11,
                fontWeight: 700,
                flexShrink: 0,
              }}
            >
              {ct.initials}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 12, fontWeight: 600 }}>{ct.authorName}</div>
              <div style={{ fontSize: 10, color: '#999' }}>{ct.task}</div>
            </div>
            <span
              style={{
                fontSize: 10,
                padding: '2px 8px',
                borderRadius: 10,
                fontWeight: 600,
                background: ts.bg,
                color: ts.color,
              }}
            >
              {ts.label}
              {ct.status === 'waiting' && ct.waitingDays ? ` (${ct.waitingDays}d)` : ''}
            </span>
          </div>
        );
      })}
    </div>
  );
}
