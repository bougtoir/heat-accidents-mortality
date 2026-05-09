import type { Paper } from '../../types/paper';

interface Props {
  paper: Paper;
}

export function TitleAuthorsPane({ paper }: Props) {
  return (
    <div>
      <div style={{ fontSize: 16, fontWeight: 700, color: '#1a3a4a', marginBottom: 8, lineHeight: 1.4 }}>
        {paper.title}
      </div>
      <div style={{ margin: '8px 0 6px', fontSize: 11, color: '#888' }}>Authors</div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
        {paper.authors.map((a, i) => (
          <div
            key={i}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 4,
              padding: '3px 10px',
              background: a.role === 'corresponding' ? '#e0f0e8' : '#f0ede6',
              border: a.role === 'corresponding' ? '1px solid #b0d8c0' : 'none',
              borderRadius: 12,
              fontSize: 11,
              color: '#555',
              fontWeight: a.role === 'corresponding' ? 600 : 400,
            }}
          >
            {a.role === 'corresponding' && (
              <span
                style={{
                  fontSize: 9,
                  background: '#2a7a8a',
                  color: 'white',
                  padding: '1px 5px',
                  borderRadius: 8,
                  fontWeight: 600,
                }}
              >
                CA
              </span>
            )}
            {a.role === 'first' && (
              <span
                style={{
                  fontSize: 9,
                  background: '#6a8a4a',
                  color: 'white',
                  padding: '1px 5px',
                  borderRadius: 8,
                  fontWeight: 600,
                }}
              >
                1st
              </span>
            )}
            {a.name}
          </div>
        ))}
      </div>
      {paper.authors.some((a) => a.affiliation) && (
        <div style={{ marginTop: 8, fontSize: 10, color: '#999', lineHeight: 1.6 }}>
          {paper.authors
            .filter((a) => a.affiliation)
            .map((a) => `${a.name}: ${a.affiliation}`)
            .join(' | ')}
        </div>
      )}
    </div>
  );
}
