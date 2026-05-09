import { useState, useEffect } from 'react';
import { useDashboard } from '../context/DashboardContext';
import type { Paper, PaperStatus } from '../types/paper';

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: '8px 10px',
  border: '1px solid #d0ccc0',
  borderRadius: 4,
  fontSize: 13,
  background: '#faf8f3',
  fontFamily: 'inherit',
  boxSizing: 'border-box',
};

const labelStyle: React.CSSProperties = {
  display: 'block',
  fontSize: 11,
  fontWeight: 700,
  textTransform: 'uppercase',
  letterSpacing: 0.5,
  color: '#888',
  marginBottom: 4,
};

function createEmptyPaper(): Paper {
  return {
    id: `paper-${Date.now()}`,
    title: '',
    shortTitle: '',
    authors: [],
    progress: { status: 'drafting', journal: '', timeline: [] },
    links: [],
    deliverables: [],
    deadlines: [],
    notes: [],
    todos: [],
    statistics: { wordCount: 0, figureCount: 0, tableCount: 0, referenceCount: 0 },
    costs: { apcPaid: 0, fundingSources: [] },
    coauthorTasks: [],
  };
}

export function AddPaperDialog() {
  const { addPaper, updatePaper, setAddPaperDialogOpen, editingPaper, setEditingPaper } = useDashboard();
  const isEditing = editingPaper !== null;

  const [title, setTitle] = useState('');
  const [shortTitle, setShortTitle] = useState('');
  const [status, setStatus] = useState<PaperStatus>('drafting');
  const [journal, setJournal] = useState('');
  const [impactFactor, setImpactFactor] = useState('');
  const [authorsStr, setAuthorsStr] = useState('');
  const [submissionDate, setSubmissionDate] = useState('');
  const [revisionDue, setRevisionDue] = useState('');
  const [repoUrl, setRepoUrl] = useState('');
  const [portalUrl, setPortalUrl] = useState('');
  const [notes, setNotes] = useState('');
  const [wordLimit, setWordLimit] = useState('');
  const [figureLimit, setFigureLimit] = useState('');
  const [tableLimit, setTableLimit] = useState('');
  const [refLimit, setRefLimit] = useState('');

  useEffect(() => {
    if (editingPaper) {
      setTitle(editingPaper.title);
      setShortTitle(editingPaper.shortTitle);
      setStatus(editingPaper.progress.status);
      setJournal(editingPaper.progress.journal);
      setImpactFactor(editingPaper.progress.impactFactor?.toString() ?? '');
      setAuthorsStr(editingPaper.authors.map((a) => `${a.name}${a.role === 'corresponding' ? '*' : ''}`).join(', '));
      setSubmissionDate(editingPaper.progress.submissionDate ?? '');
      setRevisionDue(editingPaper.progress.revisionDueDate ?? '');
      setRepoUrl(editingPaper.links.find((l) => l.category === 'repository')?.url ?? '');
      setPortalUrl(editingPaper.links.find((l) => l.category === 'submission')?.url ?? '');
      setNotes(editingPaper.notes.map((n) => n.content).join('\n'));
      setWordLimit(editingPaper.statistics.wordLimit?.toString() ?? '');
      setFigureLimit(editingPaper.statistics.figureLimit?.toString() ?? '');
      setTableLimit(editingPaper.statistics.tableLimit?.toString() ?? '');
      setRefLimit(editingPaper.statistics.referenceLimit?.toString() ?? '');
    }
  }, [editingPaper]);

  const handleClose = () => {
    setAddPaperDialogOpen(false);
    setEditingPaper(null);
  };

  const handleSave = () => {
    const authors = authorsStr
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
      .map((s) => ({
        name: s.replace('*', '').trim(),
        role: (s.includes('*') ? 'corresponding' : 'co-author') as 'corresponding' | 'co-author',
      }));

    const links = [];
    if (portalUrl) links.push({ label: `${journal || 'Journal'} Portal`, url: portalUrl, category: 'submission' as const });
    if (repoUrl) links.push({ label: repoUrl.split('/').slice(-1)[0] || 'Repository', url: repoUrl, category: 'repository' as const });

    const timeline = [];
    if (submissionDate) {
      timeline.push({ label: 'Submission', startDate: submissionDate, endDate: submissionDate, type: 'submission' as const });
    }

    const paper: Paper = isEditing
      ? {
          ...editingPaper,
          title,
          shortTitle: shortTitle || title.slice(0, 30),
          authors: authors.length > 0 ? authors : editingPaper.authors,
          progress: {
            ...editingPaper.progress,
            status,
            journal,
            impactFactor: impactFactor ? parseFloat(impactFactor) : undefined,
            submissionDate: submissionDate || editingPaper.progress.submissionDate,
            revisionDueDate: revisionDue || editingPaper.progress.revisionDueDate,
            timeline: editingPaper.progress.timeline.length > 0 ? editingPaper.progress.timeline : timeline,
          },
          links: links.length > 0 ? [...editingPaper.links.filter((l) => l.category === 'devin'), ...links] : editingPaper.links,
          statistics: {
            ...editingPaper.statistics,
            wordLimit: wordLimit ? parseInt(wordLimit) : editingPaper.statistics.wordLimit,
            figureLimit: figureLimit ? parseInt(figureLimit) : editingPaper.statistics.figureLimit,
            tableLimit: tableLimit ? parseInt(tableLimit) : editingPaper.statistics.tableLimit,
            referenceLimit: refLimit ? parseInt(refLimit) : editingPaper.statistics.referenceLimit,
          },
        }
      : {
          ...createEmptyPaper(),
          title,
          shortTitle: shortTitle || title.slice(0, 30),
          authors,
          progress: {
            status,
            journal,
            impactFactor: impactFactor ? parseFloat(impactFactor) : undefined,
            submissionDate: submissionDate || undefined,
            revisionDueDate: revisionDue || undefined,
            timeline,
          },
          links,
          notes: notes ? [{ id: `n-${Date.now()}`, content: notes, createdAt: new Date().toISOString().slice(0, 10) }] : [],
          statistics: {
            wordCount: 0,
            wordLimit: wordLimit ? parseInt(wordLimit) : undefined,
            figureCount: 0,
            figureLimit: figureLimit ? parseInt(figureLimit) : undefined,
            tableCount: 0,
            tableLimit: tableLimit ? parseInt(tableLimit) : undefined,
            referenceCount: 0,
            referenceLimit: refLimit ? parseInt(refLimit) : undefined,
          },
        };

    if (isEditing) {
      updatePaper(paper);
    } else {
      addPaper(paper);
    }
    handleClose();
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0,0,0,0.4)',
        zIndex: 500,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      onClick={(e) => e.target === e.currentTarget && handleClose()}
    >
      <div
        style={{
          background: '#fff',
          borderRadius: 10,
          width: 600,
          maxHeight: '85vh',
          overflowY: 'auto',
          boxShadow: '0 16px 48px rgba(0,0,0,0.2)',
        }}
      >
        <div
          style={{
            padding: '16px 20px',
            borderBottom: '1px solid #e8e4da',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <h2 style={{ fontSize: 16, fontWeight: 700, color: '#1a3a4a', margin: 0 }}>
            {isEditing ? 'Edit Paper' : 'Add New Paper'}
          </h2>
          <button
            onClick={handleClose}
            style={{ background: 'none', border: 'none', fontSize: 18, cursor: 'pointer', color: '#999' }}
          >
            &times;
          </button>
        </div>

        <div style={{ padding: 20 }}>
          <div style={{ marginBottom: 14 }}>
            <label style={labelStyle}>Paper Title</label>
            <input style={inputStyle} value={title} onChange={(e) => setTitle(e.target.value)} placeholder="e.g., Novel approach to..." />
          </div>

          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Short Title</label>
              <input style={inputStyle} value={shortTitle} onChange={(e) => setShortTitle(e.target.value)} placeholder="e.g., PMEA Zero-Cal" />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Status</label>
              <select style={inputStyle} value={status} onChange={(e) => setStatus(e.target.value as PaperStatus)}>
                <option value="drafting">Drafting</option>
                <option value="internal-review">Internal Review</option>
                <option value="submitted">Submitted</option>
                <option value="under-review">Under Review</option>
                <option value="revision">Revision</option>
                <option value="accepted">Accepted</option>
                <option value="published">Published</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 2 }}>
              <label style={labelStyle}>Target Journal</label>
              <input style={inputStyle} value={journal} onChange={(e) => setJournal(e.target.value)} placeholder="e.g., British Journal of Anaesthesia" />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Impact Factor</label>
              <input style={inputStyle} type="number" step="0.1" value={impactFactor} onChange={(e) => setImpactFactor(e.target.value)} placeholder="e.g., 9.1" />
            </div>
          </div>

          <div style={{ marginBottom: 14 }}>
            <label style={labelStyle}>Authors (comma-separated, * = corresponding)</label>
            <input style={inputStyle} value={authorsStr} onChange={(e) => setAuthorsStr(e.target.value)} placeholder="T. Onishi*, K. Yamada, S. Tanaka" />
          </div>

          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Submission Date</label>
              <input style={inputStyle} type="date" value={submissionDate} onChange={(e) => setSubmissionDate(e.target.value)} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Revision Due</label>
              <input style={inputStyle} type="date" value={revisionDue} onChange={(e) => setRevisionDue(e.target.value)} />
            </div>
          </div>

          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Submission Portal URL</label>
              <input style={inputStyle} value={portalUrl} onChange={(e) => setPortalUrl(e.target.value)} placeholder="https://..." />
            </div>
            <div style={{ flex: 1 }}>
              <label style={labelStyle}>Git Repository URL</label>
              <input style={inputStyle} value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} placeholder="https://github.com/..." />
            </div>
          </div>

          <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', color: '#888', marginBottom: 8 }}>
            Journal Limits
          </div>
          <div style={{ display: 'flex', gap: 12, marginBottom: 14 }}>
            <div style={{ flex: 1 }}>
              <label style={{ ...labelStyle, fontSize: 10 }}>Word Limit</label>
              <input style={inputStyle} type="number" value={wordLimit} onChange={(e) => setWordLimit(e.target.value)} placeholder="5000" />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ ...labelStyle, fontSize: 10 }}>Figure Limit</label>
              <input style={inputStyle} type="number" value={figureLimit} onChange={(e) => setFigureLimit(e.target.value)} placeholder="6" />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ ...labelStyle, fontSize: 10 }}>Table Limit</label>
              <input style={inputStyle} type="number" value={tableLimit} onChange={(e) => setTableLimit(e.target.value)} placeholder="4" />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ ...labelStyle, fontSize: 10 }}>Ref Limit</label>
              <input style={inputStyle} type="number" value={refLimit} onChange={(e) => setRefLimit(e.target.value)} placeholder="50" />
            </div>
          </div>

          {!isEditing && (
            <div style={{ marginBottom: 14 }}>
              <label style={labelStyle}>Notes</label>
              <textarea
                style={{ ...inputStyle, resize: 'vertical', minHeight: 60 }}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Initial notes about the paper..."
              />
            </div>
          )}
        </div>

        <div
          style={{
            padding: '14px 20px',
            borderTop: '1px solid #e8e4da',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: 8,
          }}
        >
          <button
            onClick={handleClose}
            style={{
              padding: '8px 20px',
              background: 'none',
              border: '1px solid #d0ccc0',
              borderRadius: 4,
              fontSize: 13,
              cursor: 'pointer',
              color: '#777',
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={!title.trim()}
            style={{
              padding: '8px 20px',
              background: title.trim() ? '#2a7a8a' : '#ccc',
              border: 'none',
              borderRadius: 4,
              fontSize: 13,
              color: 'white',
              fontWeight: 600,
              cursor: title.trim() ? 'pointer' : 'not-allowed',
            }}
          >
            {isEditing ? 'Save Changes' : 'Add Paper'}
          </button>
        </div>
      </div>
    </div>
  );
}
