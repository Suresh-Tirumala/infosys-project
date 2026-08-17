import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { documentsAPI } from '../../api/documents';
import type { UploadedDocument } from '../../types';

const DocumentUpload: React.FC = () => {
  const [documents, setDocuments] = useState<UploadedDocument[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<UploadedDocument | null>(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(true);

  React.useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await documentsAPI.list();
      setDocuments(docs);
    } catch (err) {
    } finally {
      setLoading(false);
    }
  };

  const onDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;
    setUploading(true);
    try {
      const doc = await documentsAPI.upload(acceptedFiles[0]);
      setDocuments(prev => [doc, ...prev]);
    } catch (err) {
    } finally {
      setUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt'],
      'image/png': ['.png'],
      'image/jpeg': ['.jpg', '.jpeg'],
    },
    maxSize: 10 * 1024 * 1024,
    multiple: false,
  });

  const handleAskQuestion = async () => {
    if (!selectedDoc || !question.trim()) return;
    try {
      const res = await documentsAPI.askAboutDocument(selectedDoc.id, question);
      setAnswer(res.response);
    } catch (err) {
      setAnswer('Failed to get answer. Please try again.');
    }
  };

  const handleDelete = async (docId: number) => {
    try {
      await documentsAPI.delete(docId);
      setDocuments(prev => prev.filter(d => d.id !== docId));
      if (selectedDoc?.id === docId) setSelectedDoc(null);
    } catch (err) {
    }
  };

  return (
    <div className="space-y-6">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-primary-400'
        }`}
      >
        <input {...getInputProps()} />
        <svg className="w-12 h-12 text-gray-400 mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        {uploading ? (
          <p className="text-gray-600">Uploading...</p>
        ) : (
          <>
            <p className="text-gray-600 font-medium">Drop a health document here, or click to select</p>
            <p className="text-sm text-gray-400 mt-1">PDF, TXT, PNG, JPG (max 10MB)</p>
          </>
        )}
      </div>

      {documents.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-gray-700">Uploaded Documents</h3>
          {documents.map((doc) => (
            <div
              key={doc.id}
              className={`p-4 rounded-lg border cursor-pointer transition-colors ${
                selectedDoc?.id === doc.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => { setSelectedDoc(doc); setAnswer(''); }}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                    <svg className="w-5 h-5 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-900">{doc.original_filename}</p>
                    <p className="text-xs text-gray-500">
                      {(doc.file_size / 1024).toFixed(1)} KB - {new Date(doc.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <button
                  onClick={(e) => { e.stopPropagation(); handleDelete(doc.id); }}
                  className="text-red-400 hover:text-red-600 p-1"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              {doc.summary && selectedDoc?.id === doc.id && (
                <div className="mt-3 p-3 bg-gray-50 rounded-lg text-sm text-gray-700">
                  {doc.summary}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {selectedDoc && (
        <div className="card p-4">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Ask about this document</h3>
          <div className="flex gap-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What do these lab results mean?"
              className="input-field flex-1"
              onKeyDown={(e) => e.key === 'Enter' && handleAskQuestion()}
            />
            <button onClick={handleAskQuestion} className="btn-primary">
              Ask
            </button>
          </div>
          {answer && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg text-sm text-gray-700 whitespace-pre-wrap">
              {answer}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
