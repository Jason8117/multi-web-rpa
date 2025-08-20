import { NextRequest, NextResponse } from 'next/server';
import { readFileSync } from 'fs';
import { join } from 'path';

export async function GET(request: NextRequest) {
  try {
    // 템플릿 파일 경로
    const templatePath = join(process.cwd(), '..', '..', 'data', 'template', 'iljinholdings_visit_template.xlsx');
    
    // 파일 읽기
    const fileBuffer = readFileSync(templatePath);
    
    // 응답 헤더 설정
    const response = new NextResponse(fileBuffer);
    response.headers.set('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
    response.headers.set('Content-Disposition', 'attachment; filename="iljinholdings_visit_template.xlsx"');
    response.headers.set('Content-Length', fileBuffer.length.toString());
    
    return response;
  } catch (error) {
    console.error('템플릿 파일 다운로드 오류:', error);
    return NextResponse.json(
      { error: '템플릿 파일을 찾을 수 없습니다.' },
      { status: 404 }
    );
  }
}
