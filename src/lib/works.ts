import type { CollectionEntry } from "astro:content";

export type Locale = "en" | "ja" | "zh";
export type WorkSection = "research" | "writing";

type LocalizedText = Record<Locale, string>;
type WorkEntry = CollectionEntry<"works">;

export const projectRoutes: Record<Locale, string> = {
  en: "/projects",
  ja: "/ja/projects",
  zh: "/zh/projects",
};

export const workSectionTitles: Record<Locale, Record<WorkSection, string>> = {
  en: {
    research: "Research and analysis",
    writing: "Writing and notes",
  },
  ja: {
    research: "研究と解析",
    writing: "文章作成とノート",
  },
  zh: {
    research: "研究与数据分析",
    writing: "写作与笔记",
  },
};

export const localizedText = (value: LocalizedText, locale: Locale) => value[locale] ?? value.en;

export const visibleWorks = (works: WorkEntry[], locale: Locale) =>
  works
    .filter((work) => !work.data.visibleIn || work.data.visibleIn.includes(locale))
    .sort((a, b) => {
      const diff = b.data.pubDate.valueOf() - a.data.pubDate.valueOf();
      if (diff !== 0) return diff;
      return (a.data.order ?? 0) - (b.data.order ?? 0);
    });

export const worksBySection = (works: WorkEntry[], locale: Locale, section: WorkSection) =>
  visibleWorks(works, locale).filter((work) => work.data.section === section);

export const featuredWorks = (works: WorkEntry[], locale: Locale) =>
  visibleWorks(works, locale).filter((work) => work.data.featured);

export const workCard = (work: WorkEntry, locale: Locale, options?: { useSummary?: boolean; url?: string }) => {
  const title = options?.useSummary && work.data.summaryTitle ? work.data.summaryTitle : work.data.title;
  const description = options?.useSummary && work.data.summary ? work.data.summary : work.data.description;

  return {
    title: localizedText(title, locale),
    img: work.data.heroImage,
    desc: localizedText(description, locale),
    url: options?.url ?? (work.data.projectUrl ? localizedText(work.data.projectUrl, locale) : projectRoutes[locale]),
    badge: work.data.badge,
  };
};
