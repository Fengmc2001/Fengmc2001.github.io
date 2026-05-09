// Blog post slugs that should be hidden from "Latest notes" lists across all
// locale homepages. Add a slug here if a blog post is a placeholder that you
// don't want to advertise on the home page yet (the article URL still works).
export const HIDDEN_NOTE_SLUGS: ReadonlySet<string> = new Set([
  "academic-writing",
  "reproducible-analysis",
]);

// Convenience filter to keep only public-facing posts.
export const isPublicNote = <T extends { slug: string }>(post: T) =>
  !HIDDEN_NOTE_SLUGS.has(post.slug);
