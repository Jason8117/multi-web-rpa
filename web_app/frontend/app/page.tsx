'use client';

import { useState } from 'react';

export default function Home() {
  const [selectedWebsite, setSelectedWebsite] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);

  const websites = [
    { id: 'iljin_holdings', name: '일진홀딩스', description: '방문신청 자동화' },
    { id: 'ip_168_itsm', name: 'IP 168 ITSM', description: 'ITSM 시스템 자동화' }
  ];

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const runAutomation = async () => {
    if (!selectedWebsite || !file) {
      alert('웹사이트와 엑셀 파일을 선택해주세요.');
      return;
    }

    setIsRunning(true);
    setIsCompleted(false);
    setLogs([]);

    const formData = new FormData();
    formData.append('website', selectedWebsite);
    formData.append('file', file);

    try {
      const response = await fetch('/api/run-automation', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const reader = response.body?.getReader();
        if (!reader) throw new Error('Response body is null');

        const decoder = new TextDecoder();

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          const lines = chunk.split('\n').filter(line => line.trim());
          
          setLogs(prev => [...prev, ...lines]);
          
          // 자동화 완료 확인
          if (chunk.includes('브라우저가 열린 상태로 유지됩니다') || 
              chunk.includes('자동화 테스트 성공') ||
              chunk.includes('전체 회원가입 자동화 테스트 완료')) {
            setIsCompleted(true);
          }
        }
      } else {
        throw new Error('자동화 실행 실패');
      }
    } catch (error) {
      setLogs(prev => [...prev, `오류: ${error instanceof Error ? error.message : 'Unknown error'}`]);
    } finally {
      setIsRunning(false);
    }
  };

  const resetAutomation = () => {
    setSelectedWebsite('');
    setFile(null);
    setIsCompleted(false);
    setLogs([]);
  };

  const getWebsiteDisplayName = (id: string) => {
    const website = websites.find(w => w.id === id);
    return website ? website.name : id;
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          Multi-Website RPA 시스템
        </h1>

        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-6">
          {/* 웹사이트 선택 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">웹사이트 선택</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {websites.map((website) => (
                <div
                  key={website.id}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedWebsite === website.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                  onClick={() => setSelectedWebsite(website.id)}
                >
                  <h3 className="font-semibold">{website.name}</h3>
                  <p className="text-gray-600 text-sm">{website.description}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 엑셀 템플릿 다운로드 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">엑셀 템플릿 다운로드</h2>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-blue-800">일진홀딩스 방문신청 템플릿</h3>
                  <p className="text-blue-700 text-sm mt-1">
                    방문신청에 필요한 데이터 형식을 포함한 엑셀 템플릿 파일입니다.
                  </p>
                </div>
                <button
                  onClick={() => window.open('/api/download-template', '_blank')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
                >
                  <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  템플릿 다운로드
                </button>
              </div>
            </div>
          </div>

          {/* 파일 업로드 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">엑셀 파일 업로드</h2>
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            {file && (
              <p className="mt-2 text-sm text-gray-600">
                선택된 파일: {file.name}
              </p>
            )}
          </div>

          {/* 실행 버튼 */}
          <div className="mb-6">
            <button
              onClick={runAutomation}
              disabled={isRunning || !selectedWebsite || !file}
              className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                isRunning || !selectedWebsite || !file
                  ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {isRunning ? '자동화 실행 중...' : '자동화 시작'}
            </button>
          </div>

          {/* 자동화 완료 상태 표시 */}
          {isCompleted && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center">
                <div className="w-6 h-6 bg-green-500 rounded-full mr-3 flex items-center justify-center">
                  <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-semibold text-green-800">
                    ✅ {getWebsiteDisplayName(selectedWebsite)} 자동화 완료!
                  </h3>
                  <p className="text-green-700 text-sm mt-1">
                    브라우저가 열린 상태로 유지됩니다. 웹에서 직접 다음 작업을 진행할 수 있습니다.
                  </p>
                </div>
              </div>
              <div className="mt-3 flex space-x-2">
                <button
                  onClick={resetAutomation}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  새 자동화 시작
                </button>
                <button
                  onClick={() => window.open('http://localhost:3000', '_blank')}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  새 탭에서 열기
                </button>
              </div>
            </div>
          )}

          {/* 로그 출력 */}
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-4">실행 로그</h2>
            <div className="bg-gray-900 text-green-400 p-4 rounded-lg h-96 overflow-y-auto font-mono text-sm">
              {logs.length === 0 ? (
                <p className="text-gray-500">로그가 여기에 표시됩니다...</p>
              ) : (
                logs.map((log, index) => (
                  <div key={index} className="mb-1">
                    {log}
                  </div>
                ))
              )}
            </div>
          </div>

          {/* 상태 표시 */}
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-medium">
              {isRunning ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                  자동화 실행 중...
                </>
              ) : isCompleted ? (
                <>
                  <div className="w-4 h-4 bg-green-500 rounded-full mr-2"></div>
                  자동화 완료
                </>
              ) : (
                <>
                  <div className="w-4 h-4 bg-gray-400 rounded-full mr-2"></div>
                  대기 중
                </>
              )}
            </div>
          </div>

          {/* 사용법 안내 */}
          <div className="mt-8 p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-800 mb-2">💡 사용법 안내</h3>
            <ul className="text-blue-700 text-sm space-y-1">
              <li>• 1단계: 자동화할 웹사이트를 선택하세요</li>
              <li>• 2단계: 엑셀 템플릿을 다운로드하여 데이터를 입력하세요</li>
              <li>• 3단계: 작성된 엑셀 데이터 파일을 업로드하세요</li>
              <li>• 4단계: "자동화 시작" 버튼을 클릭하세요</li>
              <li>• 5단계: 자동화가 완료되면 브라우저가 열린 상태로 유지됩니다</li>
              <li>• 6단계: 웹에서 직접 다음 작업을 진행할 수 있습니다</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  );
}
