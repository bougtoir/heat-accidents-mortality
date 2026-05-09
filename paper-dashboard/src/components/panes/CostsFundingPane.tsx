import type { Paper } from '../../types/paper';

interface Props {
  paper: Paper;
}

function formatCurrency(amount: number, currency: string): string {
  const symbols: Record<string, string> = { GBP: '\u00A3', USD: '$', JPY: '\u00A5', EUR: '\u20AC' };
  const sym = symbols[currency] ?? currency + ' ';
  return `${sym}${amount.toLocaleString()}`;
}

export function CostsFundingPane({ paper }: Props) {
  const c = paper.costs;
  const apcCurrency = c.apcCurrency ?? 'USD';
  const outstanding = (c.apcEstimate ?? 0) - c.apcPaid;

  return (
    <div>
      {(c.apcEstimate ?? 0) > 0 && (
        <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
          <div
            style={{
              flex: 1,
              padding: 10,
              background: '#faf8f3',
              borderRadius: 4,
              border: '1px solid #e8e4da',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: 18, fontWeight: 700, color: '#1a3a4a' }}>
              {formatCurrency(c.apcEstimate ?? 0, apcCurrency)}
            </div>
            <div style={{ fontSize: 10, color: '#888' }}>APC Estimate</div>
          </div>
          <div
            style={{
              flex: 1,
              padding: 10,
              background: '#faf8f3',
              borderRadius: 4,
              border: '1px solid #e8e4da',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: 18, fontWeight: 700, color: '#40a060' }}>
              {formatCurrency(c.apcPaid, apcCurrency)}
            </div>
            <div style={{ fontSize: 10, color: '#888' }}>Paid</div>
          </div>
          <div
            style={{
              flex: 1,
              padding: 10,
              background: '#faf8f3',
              borderRadius: 4,
              border: '1px solid #e8e4da',
              textAlign: 'center',
            }}
          >
            <div style={{ fontSize: 18, fontWeight: 700, color: outstanding > 0 ? '#d04040' : '#40a060' }}>
              {formatCurrency(outstanding, apcCurrency)}
            </div>
            <div style={{ fontSize: 10, color: '#888' }}>Outstanding</div>
          </div>
        </div>
      )}

      {c.fundingSources.length > 0 ? (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              {['Funding Source', 'Budget', 'Allocated', 'Status'].map((h) => (
                <th
                  key={h}
                  style={{
                    textAlign: 'left',
                    fontSize: 10,
                    fontWeight: 700,
                    textTransform: 'uppercase',
                    letterSpacing: 0.5,
                    color: '#888',
                    padding: '4px 8px 6px',
                    borderBottom: '2px solid #d0ccc0',
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {c.fundingSources.map((fs, i) => (
              <tr key={i}>
                <td
                  style={{
                    padding: '7px 8px',
                    fontSize: 12,
                    borderBottom: '1px solid #f0ede6',
                    background: i % 2 === 1 ? '#faf8f3' : undefined,
                  }}
                >
                  {fs.name}
                </td>
                <td
                  style={{
                    padding: '7px 8px',
                    fontSize: 12,
                    borderBottom: '1px solid #f0ede6',
                    background: i % 2 === 1 ? '#faf8f3' : undefined,
                  }}
                >
                  {formatCurrency(fs.budget, fs.currency)}
                </td>
                <td
                  style={{
                    padding: '7px 8px',
                    fontSize: 12,
                    borderBottom: '1px solid #f0ede6',
                    background: i % 2 === 1 ? '#faf8f3' : undefined,
                  }}
                >
                  {formatCurrency(fs.allocated, fs.currency)}
                </td>
                <td
                  style={{
                    padding: '7px 8px',
                    fontSize: 12,
                    borderBottom: '1px solid #f0ede6',
                    background: i % 2 === 1 ? '#faf8f3' : undefined,
                  }}
                >
                  <span
                    style={{
                      color: fs.status === 'approved' ? '#40a060' : fs.status === 'pending' ? '#d09030' : '#c04040',
                      fontWeight: 600,
                    }}
                  >
                    {fs.status.charAt(0).toUpperCase() + fs.status.slice(1)}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div style={{ color: '#aaa', fontSize: 12 }}>No funding sources configured</div>
      )}
    </div>
  );
}
