import type { Paper } from '../../types/paper';
import { StatusBadge } from '../common/StatusBadge';
import { GanttChart } from '../common/GanttChart';

interface Props {
  paper: Paper;
}

export function ProgressPane({ paper }: Props) {
  const p = paper.progress;
  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10 }}>
        <StatusBadge status={p.status} />
        <span style={{ fontSize: 11, color: '#888' }}>
          {p.journal}
          {p.impactFactor ? ` \u2022 IF: ${p.impactFactor}` : ''}
        </span>
      </div>
      <GanttChart events={p.timeline} />
      <div style={{ marginTop: 10, display: 'flex', gap: 16, fontSize: 10, color: '#aaa' }}>
        {p.submissionDate && <span>Submitted: {p.submissionDate}</span>}
        {p.revisionDueDate && (
          <span style={{ color: '#d08050', fontWeight: 600 }}>Revision due: {p.revisionDueDate}</span>
        )}
        {p.acceptanceDate && <span style={{ color: '#40a060' }}>Accepted: {p.acceptanceDate}</span>}
      </div>
    </div>
  );
}
