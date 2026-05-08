import { z, defineCollection } from "astro:content";

const localeTextSchema = z.object({
    en: z.string(),
    ja: z.string(),
    zh: z.string(),
});

const blogSchema = z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.string().optional(),
    heroImage: z.string().optional(),
    badge: z.string().optional(),
    tags: z.array(z.string()).refine(items => new Set(items).size === items.length, {
        message: 'tags must be unique',
    }).optional(),
});

export type BlogSchema = z.infer<typeof blogSchema>;

const blogCollection = defineCollection({ schema: blogSchema });

const workSchema = z.object({
    title: localeTextSchema,
    description: localeTextSchema,
    summaryTitle: localeTextSchema.optional(),
    summary: localeTextSchema.optional(),
    section: z.enum(["research", "writing"]),
    badge: z.string(),
    heroImage: z.string().optional(),
    projectUrl: localeTextSchema.optional(),
    order: z.number(),
    featured: z.boolean().default(false),
    visibleIn: z.array(z.enum(["en", "ja", "zh"])).optional(),
});

export type WorkSchema = z.infer<typeof workSchema>;

const worksCollection = defineCollection({ schema: workSchema });

export const collections = {
    'blog': blogCollection,
    'works': worksCollection,
}
