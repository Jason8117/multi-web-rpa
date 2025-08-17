import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { join } from 'path';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const website = formData.get('website') as string;
    const file = formData.get('file') as File;

    if (!website || !file) {
      return NextResponse.json(
        { error: '웹사이트와 파일이 필요합니다.' },
        { status: 400 }
      );
    }

    // 파일을 임시로 저장
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const filePath = join(process.cwd(), 'temp', file.name);
    
    // temp 디렉토리 생성
    const tempDir = join(process.cwd(), 'temp');
    if (!existsSync(tempDir)) {
      mkdirSync(tempDir, { recursive: true });
    }
    
    writeFileSync(filePath, buffer);

    // 스트리밍 응답 생성
    const stream = new ReadableStream({
      start(controller) {
        const projectRoot = join(process.cwd(), '../..');
        const pythonPath = join(projectRoot, 'venv', 'bin', 'python');
        const mainScriptPath = join(projectRoot, 'src', 'main.py');
        
        console.log('Python 경로:', pythonPath);
        console.log('메인 스크립트 경로:', mainScriptPath);
        console.log('작업 디렉토리:', projectRoot);
        console.log('선택된 웹사이트:', website);
        console.log('입력 파일:', filePath);
        
        let isControllerClosed = false;
        
        // 웹 모드로 실행하여 브라우저 유지
        const pythonProcess = spawn(pythonPath, [
          mainScriptPath,
          '--website', website,
          '--test',
          '--input-file', filePath,
          '--web-mode'
        ], {
          cwd: projectRoot,
          env: {
            ...process.env,
            PYTHONPATH: projectRoot
          }
        });

        // 안전한 enqueue 함수
        const safeEnqueue = (text: string) => {
          if (!isControllerClosed) {
            try {
              controller.enqueue(new TextEncoder().encode(text));
            } catch (error) {
              console.error('Controller enqueue 오류:', error);
              isControllerClosed = true;
            }
          }
        };

        // stdout 처리
        pythonProcess.stdout.on('data', (data) => {
          const text = data.toString();
          safeEnqueue(text);
        });

        // stderr 처리
        pythonProcess.stderr.on('data', (data) => {
          const text = data.toString();
          safeEnqueue(`ERROR: ${text}`);
        });

        // 프로세스 종료 처리
        pythonProcess.on('close', (code) => {
          safeEnqueue(`\n🎉 자동화 프로세스가 완료되었습니다! (코드: ${code})\n`);
          safeEnqueue(`🌐 브라우저가 열린 상태로 유지됩니다.\n`);
          safeEnqueue(`💡 웹에서 직접 다음 작업을 진행할 수 있습니다.\n`);
          safeEnqueue(`📝 자동화 결과를 확인하고 필요한 경우 수동으로 조정하세요.\n`);
          safeEnqueue(`⚠️  브라우저를 닫으려면 수동으로 닫기 버튼을 클릭하세요.\n`);
          isControllerClosed = true;
          controller.close();
          
          // 임시 파일 삭제
          try {
            unlinkSync(filePath);
          } catch (error) {
            console.error('임시 파일 삭제 실패:', error);
          }
        });

        // 오류 처리
        pythonProcess.on('error', (error) => {
          safeEnqueue(`❌ 오류가 발생했습니다: ${error.message}\n`);
          safeEnqueue(`🌐 브라우저는 열린 상태로 유지됩니다.\n`);
          safeEnqueue(`💡 오류를 확인하고 필요한 경우 수동으로 작업을 진행하세요.\n`);
          isControllerClosed = true;
          controller.close();
        });
      }
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });

  } catch (error) {
    console.error('API 오류:', error);
    return NextResponse.json(
      { error: '서버 오류가 발생했습니다.' },
      { status: 500 }
    );
  }
}
