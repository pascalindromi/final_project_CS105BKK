from baboonmod import typingcore

if __name__ == "__main__":
    target_text = "The quick brown fox jumps over the lazy dog."

    results = typingcore.run_typing_test(target_text)

    if not results:
        print("\nTest ended.")
        
    else:
        print("\nTest finished!")
        print(f"Your input: {results['typed_text']}")
        print(f"Total mistakes: {results['total_mistakes']}")
        print(f"Elapsed time: {results['elapsed']:.2f}s")