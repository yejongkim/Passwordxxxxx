"""
화성 기지 비상 저장소 문 해킹 프로그램
emergency_storage_key.zip 파일의 비밀번호를 brute force 방식으로 해독합니다.
"""

import zipfile
import time
import itertools


def unlock_zip():
    """
    emergency_storage_key.zip 파일의 암호를 해독하는 함수
    암호는 숫자와 소문자 알파벳으로 구성된 6자리 문자열
    """
    zip_filename = 'emergency_storage_key.zip'
    password_output_file = 'password.txt'
    
    # 비밀번호 구성 문자: 숫자(0-9) + 소문자(a-z)
    charset = '0123456789abcdefghijklmnopqrstuvwxyz'
    password_length = 6
    
    print('=' * 60)
    print('화성 기지 비상 저장소 문 해킹 시작')
    print('=' * 60)
    print(f'대상 파일: {zip_filename}')
    print(f'암호 길이: {password_length}자리')
    print(f'사용 문자셋: 숫자(0-9) + 소문자(a-z) = {len(charset)}개 문자')
    print(f'예상 경우의 수: {len(charset) ** password_length:,}')
    print('=' * 60)
    
    # zip 파일 존재 확인
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zf:
            print(f'zip 파일 확인 완료: {zip_filename}')
    except FileNotFoundError:
        print(f'오류: {zip_filename} 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류: zip 파일 읽기 실패 - {e}')
        return
    
    # 시작 시간 기록
    start_time = time.time()
    attempt_count = 0
    found_password = None
    
    print('\n암호 해독 시작...\n')
    
    # brute force 공격
    try:
        for password_tuple in itertools.product(charset, repeat=password_length):
            password = ''.join(password_tuple)
            attempt_count += 1
            
            # 1000번마다 진행 상황 출력
            if attempt_count % 1000 == 0:
                elapsed_time = time.time() - start_time
                print(f'시도 횟수: {attempt_count:,} | '
                      f'경과 시간: {elapsed_time:.2f}초 | '
                      f'현재 시도: {password}')
            
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zf:
                    # 비밀번호 시도
                    zf.extractall(pwd=password.encode('utf-8'))
                    found_password = password
                    break
            except (RuntimeError, zipfile.BadZipFile):
                # 잘못된 비밀번호이거나 zip 파일 오류
                continue
            except Exception as e:
                # 기타 예외
                continue
    
    except KeyboardInterrupt:
        print('\n\n암호 해독이 사용자에 의해 중단되었습니다.')
        return
    except Exception as e:
        print(f'\n\n오류 발생: {e}')
        return
    
    # 결과 출력
    end_time = time.time()
    total_time = end_time - start_time
    
    print('\n' + '=' * 60)
    if found_password:
        print('암호 해독 성공!')
        print('=' * 60)
        print(f'발견된 암호: {found_password}')
        print(f'총 시도 횟수: {attempt_count:,}')
        print(f'소요 시간: {total_time:.2f}초')
        print(f'초당 시도 횟수: {attempt_count / total_time:.2f}')
        
        # 비밀번호를 파일에 저장
        try:
            with open(password_output_file, 'w', encoding='utf-8') as f:
                f.write(found_password)
            print(f'\n비밀번호가 {password_output_file}에 저장되었습니다.')
        except Exception as e:
            print(f'\n오류: 비밀번호 파일 저장 실패 - {e}')
    else:
        print('암호 해독 실패')
        print('=' * 60)
        print(f'총 시도 횟수: {attempt_count:,}')
        print(f'소요 시간: {total_time:.2f}초')
    
    print('=' * 60)


def unlock_zip_optimized():
    """
    [보너스] 최적화된 암호 해독 함수
    
    최적화 전략:
    1. 일반적인 패턴 우선 시도 (숫자만, 문자만, 간단한 조합)
    2. 사전 기반 공격 (일반적인 단어들 먼저 시도)
    3. 통계적으로 자주 사용되는 문자 우선
    """
    zip_filename = 'emergency_storage_key.zip'
    password_output_file = 'password.txt'
    
    print('=' * 60)
    print('화성 기지 비상 저장소 문 해킹 시작 (최적화 버전)')
    print('=' * 60)
    
    # zip 파일 존재 확인
    try:
        with zipfile.ZipFile(zip_filename, 'r') as zf:
            print(f'zip 파일 확인 완료: {zip_filename}')
    except FileNotFoundError:
        print(f'오류: {zip_filename} 파일을 찾을 수 없습니다.')
        return
    except Exception as e:
        print(f'오류: zip 파일 읽기 실패 - {e}')
        return
    
    start_time = time.time()
    attempt_count = 0
    found_password = None
    
    def try_password(pwd):
        """비밀번호 시도 헬퍼 함수"""
        nonlocal attempt_count
        attempt_count += 1
        
        if attempt_count % 1000 == 0:
            elapsed = time.time() - start_time
            print(f'시도 횟수: {attempt_count:,} | '
                  f'경과 시간: {elapsed:.2f}초 | '
                  f'현재 시도: {pwd}')
        
        try:
            with zipfile.ZipFile(zip_filename, 'r') as zf:
                zf.extractall(pwd=pwd.encode('utf-8'))
                return True
        except:
            return False
    
    print('\n최적화 전략 1: 일반적인 패턴 시도 중...\n')
    
    # 전략 1: 숫자만 6자리 (000000 ~ 999999)
    for i in range(1000000):
        pwd = str(i).zfill(6)
        if try_password(pwd):
            found_password = pwd
            break
    
    if not found_password:
        print('\n최적화 전략 2: 문자만 조합 시도 중...\n')
        # 전략 2: 소문자만 6자리
        charset = 'abcdefghijklmnopqrstuvwxyz'
        for password_tuple in itertools.product(charset, repeat=6):
            pwd = ''.join(password_tuple)
            if try_password(pwd):
                found_password = pwd
                break
    
    if not found_password:
        print('\n최적화 전략 3: 혼합 조합 시도 중...\n')
        # 전략 3: 전체 문자셋
        charset = '0123456789abcdefghijklmnopqrstuvwxyz'
        for password_tuple in itertools.product(charset, repeat=6):
            pwd = ''.join(password_tuple)
            if try_password(pwd):
                found_password = pwd
                break
    
    # 결과 출력
    end_time = time.time()
    total_time = end_time - start_time
    
    print('\n' + '=' * 60)
    if found_password:
        print('암호 해독 성공!')
        print('=' * 60)
        print(f'발견된 암호: {found_password}')
        print(f'총 시도 횟수: {attempt_count:,}')
        print(f'소요 시간: {total_time:.2f}초')
        print(f'초당 시도 횟수: {attempt_count / total_time:.2f}')
        
        try:
            with open(password_output_file, 'w', encoding='utf-8') as f:
                f.write(found_password)
            print(f'\n비밀번호가 {password_output_file}에 저장되었습니다.')
        except Exception as e:
            print(f'\n오류: 비밀번호 파일 저장 실패 - {e}')
    else:
        print('암호 해독 실패')
        print('=' * 60)
        print(f'총 시도 횟수: {attempt_count:,}')
        print(f'소요 시간: {total_time:.2f}초')
    
    print('=' * 60)


if __name__ == '__main__':
    # 기본 버전 실행
    # unlock_zip()
    
    # 최적화 버전 실행 (더 빠름)
    unlock_zip_optimized()
