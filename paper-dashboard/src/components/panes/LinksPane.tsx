import type { Paper } from '../../types/paper';

const CATEGORY_LABELS: Record<string, string> = {
  submission: 'Submission Portal',
  devin: 'Devin Sessions',
  repository: 'Repository',
  other: 'Other',
};

const CATEGORY_ICONS: Record<string, string> = {
  submission: '\uD83C\uDF10',
  devin: '\u2699',
  repository: '\uD83D\uDCC1',
  other: '\uD83D\uDD17',
};

interface Props {
  paper: Paper;
}

export function LinksPane({ paper }: Props) {
  const grouped = paper.links.reduce(
    (acc, link) => {
      const cat = link.category;
      if (!acc[cat]) acc[cat] = [];
      acc[cat].push(link);
      return acc;
    },
    {} as Record<string, typeof paper.links>,
  );

  if (paper.links.length === 0) {
    return <div style={{ color: '#aaa', fontSize: 12 }}>No links added</div>;
  }

  return (
    <div>
      {Object.entries(grouped).map(([cat, links]) => (
        <div key={cat} style={{ marginBottom: 10 }}>
          <div
            style={{
              fontSize: 10,
              fontWeight: 700,
              textTransform: 'uppercase',
              color: '#888',
              marginBottom: 4,
              letterSpacing: 0.5,
            }}
          >
            {CATEGORY_LABELS[cat] ?? cat}
          </div>
          {links.map((link, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '4px 0', fontSize: 12 }}>
              <span style={{ fontSize: 14 }}>{CATEGORY_ICONS[cat] ?? '\uD83D\uDD17'}</span>
              <a
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#2a7a8a', textDecoration: 'none' }}
              >
                {link.label}
              </a>
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}
