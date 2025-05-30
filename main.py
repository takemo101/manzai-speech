import os
import wave
from dataclasses import dataclass

from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()


# Waveファイルを保存するための設定
def wave_file(
    filename: str,
    pcm: bytes,
    channels: int = 1,
    rate: int = 24000,
    sample_width: int = 2,
):
    """PCMデータをWaveファイルに保存します。"""
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)


def generate_content(client: Client, prompt: str) -> str:
    """Gemini APIを使用して、指定されたプロンプトからコンテンツを生成します。"""
    content_response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction="""
            あなたはベテラン漫才師です。30秒の漫才のスクリプトを生成してください。
            以下の形式のみで出力してください。
            登場人物名: [セリフ]
            例:
            A: こんにちは、Bさん。今日はどんなことをしていますか？
            B: こんにちは、Aさん。今日は新しいプロジェクトのアイデアを考えていました。
            """,
            temperature=0.1,
        ),
    )

    content = content_response.text

    if not content:
        raise ValueError('APIからコンテンツが受信されませんでした。')

    print(f'生成されたコンテンツ:\n{content}')
    return content


@dataclass(frozen=True)
class SpeakerSetting:
    """スピーカーの設定を表すデータクラス。"""

    speaker: str  # スピーカーの名前
    voice_name: str  # 使用する音声の名前 example: 'Leda', 'Gacrux'


def generate_audio(
    client: Client, content: str, speakers: list[SpeakerSetting]
) -> bytes:
    """Gemini APIを使用して、指定されたコンテンツから音声を生成します。"""
    voice_response = client.models.generate_content(
        model='gemini-2.5-flash-preview-tts',
        contents=content,
        config=types.GenerateContentConfig(
            response_modalities=['AUDIO'],
            speech_config=types.SpeechConfig(
                multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                    speaker_voice_configs=[
                        types.SpeakerVoiceConfig(
                            speaker=speaker.speaker,
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name=speaker.voice_name,
                                )
                            ),
                        )
                        for speaker in speakers
                    ]
                )
            ),
        ),
    )

    candidates = voice_response.candidates

    # ガード句: 応答が存在し、音声データが含まれているか確認
    if (
        candidates
        and candidates[0].content
        and candidates[0].content.parts
        and candidates[0].content.parts[0].inline_data
    ):
        data = candidates[0].content.parts[0].inline_data.data
    else:
        raise ValueError('APIから音声データが受信されませんでした。')

    if not data:
        raise ValueError('APIから音声データが受信されませんでした。')

    print('音声生成中...')
    print(f'音声データの長さ: {len(data)} バイト')
    return data


def main():
    client = Client(api_key=os.getenv('GEMINI_API_KEY'))

    # コンテンツ生成の実行
    content = generate_content(client, 'taniとtakedaの漫才を生成してください')

    # 音声の生成
    data = generate_audio(
        client,
        content,
        # スピーカーごとの音声設定を指定
        speakers=[
            SpeakerSetting(speaker='tani', voice_name='Leda'),
            SpeakerSetting(speaker='takeda', voice_name='Gacrux'),
        ],
    )

    # 生成された音声データをwaveファイルとして保存
    wave_file('output.wav', data)


if __name__ == '__main__':
    main()
