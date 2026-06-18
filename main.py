"""
LinkedIn Content Creation Agent
"""

from src.generator import generate_post
from src.researcher import research_and_generate
from src.utils import save_output
from src.config import POST_TYPE_MAP


def _display_result(result: dict) -> None:
    print("\n" + "=" * 60)
    print("LINKEDIN POST")
    print("=" * 60)
    print(result["post"])
    print("\n" + "=" * 60)
    print("IMAGE CONCEPT")
    print("=" * 60)
    print(result["image_concept"])


def main() -> None:
    print("=" * 60)
    print("  NB MEDIA — LinkedIn Content Creation Agent")
    print("  Generates posts in Nikit Bassi's exact style")
    print("=" * 60)

    print("\nChoose mode:")
    print("  1. User Input  — provide a topic manually")
    print("  2. Auto Research — scrape trending topics via Tavily")
    mode = input("\nEnter 1 or 2: ").strip()

    if mode == "1":
        topic = input("\nEnter your topic or idea:\n> ").strip()

        print("\nPost type (press Enter to auto-detect):")
        print("  1. NB Media Internal Story")
        print("  2. Founder Spotlight")
        print("  3. AI Tool Breakdown")
        print("  4. Contrarian Take")
        type_choice = input("Enter 1-4 or press Enter: ").strip()

        post_type = POST_TYPE_MAP.get(type_choice, "auto")

        print("\nGenerating post...")
        result = generate_post(topic, post_type)

    elif mode == "2":
        niche = input(
            "\nEnter niche/industry (default: AI automation for businesses):\n> "
        ).strip() or "AI automation for businesses"

        print("\nResearching trending topics and generating post...")
        result = research_and_generate(niche)
        print(f"\nAuto-selected topic: {result['topic']}")

    else:
        print("Invalid choice. Exiting.")
        return

    _display_result(result)

    if input("\n\nSave this output? (y/n): ").strip().lower() == "y":
        save_output(result)


if __name__ == "__main__":
    main()
