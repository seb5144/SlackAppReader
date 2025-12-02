import os
from slack_sdk import WebClient
from collections import Counter

# ==========================================
# 👇 3단계에서 받은 'xoxp-'로 시작하는 토큰을 넣으세요
USER_TOKEN = os.get_env('SLACK_TOKEN')

# 👇 4단계에서 찾은 채널 ID를 넣으세요
TARGET_CHANNEL_ID = os.get_env('CHANNEL_ID')
# ==========================================

# 클라이언트 초기화
client = WebClient(token=USER_TOKEN)

def analyze_emoji_champions():
    reaction_counter = Counter()
    
    print(f"🕵️ 채널({TARGET_CHANNEL_ID})의 데이터를 분석합니다...")
    print("참고: 사용자 토큰을 사용하므로 봇을 초대할 필요가 없습니다.")

    try:
        # 메시지 가져오기 (기본 1000개 설정)
        # 만약 더 과거까지 보고 싶으면 limit를 늘리거나 반복문을 써야 합니다.
        response = client.conversations_history(channel=TARGET_CHANNEL_ID, limit=1000)
        messages = response['messages']
        
        print(f"📚 최근 {len(messages)}개의 메시지를 읽어왔습니다.")

        for msg in messages:
            # 리액션이 달려있는지 확인
            if 'reactions' in msg:
                for reaction in msg['reactions']:
                    # 해당 리액션을 누른 사람들 리스트
                    users = reaction['users']
                    reaction_counter.update(users)
        
        print("\n" + "="*30)
        print("🏆 이 구역의 리액션 왕은 누구? 🏆")
        print("="*30)
        
        # 상위 10명 출력
        rank = 1
        for user_id, count in reaction_counter.most_common(10):
            try:
                # 사용자 ID로 내 이름이나 동료 이름 찾기
                user_info = client.users_info(user=user_id)
                user_name = user_info['user']['real_name']
                print(f"{rank}위: {user_name} - {count}회")
                rank += 1
            except Exception:
                # 퇴사자이거나 정보를 읽을 수 없는 경우
                print(f"{rank}위: 알 수 없음({user_id}) - {count}회")
                rank += 1

    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        if "missing_scope" in str(e):
            print("👉 'User Token Scopes' 설정에서 channels:history 등을 빼먹지 않았는지 확인하세요.")
        elif "not_in_channel" in str(e):
            print("👉 본인이 해당 채널에 들어가 있는지 확인하세요. (사용자 토큰은 내가 없는 방은 못 봅니다)")

if __name__ == "__main__":
    analyze_emoji_champions()
