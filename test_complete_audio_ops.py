"""Comprehensive test suite for audio-ops.py v1.0.0"""
import sys
sys.path.insert(0, '.')
sys.path.insert(0, 'src')

import importlib.util
spec = importlib.util.spec_from_file_location("audio_ops", "library/media-operations/audio-ops.py")
audio_ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audio_ops)

from pathlib import Path

# Import all functions
transcribe_audio = audio_ops.transcribe_audio
text_to_speech = audio_ops.text_to_speech
batch_transcribe = audio_ops.batch_transcribe
transcribe_with_timestamps = audio_ops.transcribe_with_timestamps
detect_language = audio_ops.detect_language
list_voices = audio_ops.list_voices

def test_all_functions():
    """Test all 6 functions in sequence"""
    
    results = {}
    test_files = []
    
    print("🧪 Audio-Ops v1.0.0 Complete Test Suite")
    print("=" * 60)
    
    # Test 1: list_voices
    print("\n[1/6] Testing list_voices()...")
    result = list_voices()
    results['list_voices'] = result['success']
    if result['success']:
        print(f"✅ Found {result['data']['total_count']} voices")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Test 2: text_to_speech
    print("\n[2/6] Testing text_to_speech()...")
    test_text = "Hello world, this is a comprehensive test."
    result = text_to_speech(test_text, output_file="test/final_test.mp3", voice="nova")
    results['text_to_speech'] = result['success']
    if result['success']:
        test_files.append(result['data']['file_path'])
        print(f"✅ Generated {result['data']['file_size_mb']}MB audio")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Test 3: transcribe_audio
    print("\n[3/6] Testing transcribe_audio()...")
    if test_files:
        result = transcribe_audio(test_files[0])
        results['transcribe_audio'] = result['success']
        if result['success']:
            print(f"✅ Transcribed: {result['data']['text']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
    else:
        results['transcribe_audio'] = False
        print("❌ Skipped (no test file)")
    
    # Test 4: detect_language
    print("\n[4/6] Testing detect_language()...")
    if test_files:
        result = detect_language(test_files[0])
        results['detect_language'] = result['success']
        if result['success']:
            print(f"✅ Detected: {result['data']['language']}")
        else:
            print(f"❌ Failed: {result.get('error')}")
    else:
        results['detect_language'] = False
        print("❌ Skipped (no test file)")
    
    # Test 5: transcribe_with_timestamps
    print("\n[5/6] Testing transcribe_with_timestamps()...")
    if test_files:
        result = transcribe_with_timestamps(test_files[0])
        results['transcribe_with_timestamps'] = result['success']
        if result['success']:
            print(f"✅ Got {len(result['data']['segments'])} segments, {result['data']['duration']:.2f}s")
        else:
            print(f"❌ Failed: {result.get('error')}")
    else:
        results['transcribe_with_timestamps'] = False
        print("❌ Skipped (no test file)")
    
    # Test 6: batch_transcribe
    print("\n[6/6] Testing batch_transcribe()...")
    # Create 2 more test files
    batch_files = []
    for i in range(2):
        result = text_to_speech(f"Batch test number {i+1}", output_file=f"test/batch_{i}.mp3", voice="alloy")
        if result['success']:
            batch_files.append(result['data']['file_path'])
    
    if batch_files:
        result = batch_transcribe(batch_files)
        results['batch_transcribe'] = result['success']
        if result['success']:
            print(f"✅ Processed {result['data']['successful']}/{result['data']['total_files']} files")
        else:
            print(f"❌ Failed: {result.get('error')}")
        test_files.extend(batch_files)
    else:
        results['batch_transcribe'] = False
        print("❌ Skipped (couldn't create batch files)")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    for file in test_files:
        Path(file).unlink(missing_ok=True)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for func, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {func:30s} {status}")
    
    print(f"\n{'='*60}")
    print(f"🎯 Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! audio-ops.py v1.0.0 is ready!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    return results

if __name__ == "__main__":
    test_all_functions()
