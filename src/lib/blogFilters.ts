// Blog post slugs that should be hidden from "Latest notes" lists across all
// locale homepages. Add a slug here if a blog post is a placeholder that you
// don't want to advertise on the home page yet (the article URL still works).
export const HIDDEN_NOTE_SLUGS: ReadonlySet<string> = new Set([]);

type NoteLocale = "en" | "ja" | "zh";
type TranslatableNote = {
  data: { locale?: NoteLocale; translationGroup?: string };
};

// Select one version per explicit translation group BEFORE sorting/pagination.
// Ungrouped (legacy/single-language) notes remain visible in every locale.
// Incomplete groups fall back to English, then their first available version.
// This is a listing selector only: article routes must retain every entry.
export function notesForLocale<T extends TranslatableNote>(posts: T[], locale: NoteLocale): T[] {
  const selected = new Map<string, T>();
  const rank = (post: T) => post.data.locale === locale ? 2 : post.data.locale === "en" ? 1 : 0;
  for (const post of posts) {
    const group = post.data.translationGroup;
    if (!group) continue;
    const previous = selected.get(group);
    if (!previous || rank(post) > rank(previous)) selected.set(group, post);
  }
  return posts.filter((post) => !post.data.translationGroup || selected.get(post.data.translationGroup) === post);
}

// Convenience filter to keep only public-facing posts.
export const isPublicNote = <T extends { slug: string }>(post: T) =>
  !HIDDEN_NOTE_SLUGS.has(post.slug);
