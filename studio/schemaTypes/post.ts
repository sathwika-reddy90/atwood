import { defineArrayMember, defineField, defineType } from "sanity";

/** Warns (doesn't block) when an image is smaller than the size it is shown at.
 *  Asset refs encode the original size: image-<hash>-<w>x<h>-<ext>. */
const minSize = (minW: number, minH: number) => (rule: any) =>
  rule
    .custom((value: { asset?: { _ref?: string } } | undefined) => {
      const size = value?.asset?._ref?.match(/-(\d+)x(\d+)-/);
      if (!size) return true;
      const [width, height] = [Number(size[1]), Number(size[2])];
      return width >= minW && height >= minH
        ? true
        : `This image is ${width} × ${height}. Under ${minW} × ${minH} it will look blurry.`;
    })
    .warning();

const altField = defineField({
  name: "alt",
  title: "Alt text",
  type: "string",
  description: "Describe the image for screen readers and Google Images.",
  validation: (rule) => rule.required(),
});

export const post = defineType({
  name: "post",
  title: "Journal post",
  type: "document",
  // "All fields" stays the default view; the tab just gathers the SEO fields.
  groups: [{ name: "seo", title: "SEO" }],
  fields: [
    defineField({
      name: "title",
      title: "Title",
      type: "string",
      description: "The page's H1.",
      validation: (rule) => rule.required().max(120),
    }),
    defineField({
      name: "slug",
      title: "Slug",
      type: "slug",
      description: "The URL: atwooddsigns.com/journal-<slug>.html — don't change it after publishing.",
      options: { source: "title", maxLength: 96 },
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: "excerpt",
      title: "Excerpt",
      type: "text",
      rows: 3,
      description:
        "One or two sentences for the Journal cards. Also the search description when Meta description is empty.",
      validation: (rule) => rule.required().max(300),
    }),
    defineField({
      name: "seoTitle",
      title: "SEO meta title",
      type: "string",
      group: "seo",
      description:
        'The <title> shown in Google and browser tabs, used exactly as written — include "| Atwood Dsigns" yourself. Empty uses "<Title> | Atwood Dsigns".',
      validation: (rule) => [
        rule.max(70),
        rule.max(60).warning("Over 60 characters may be cut off in search results."),
      ],
    }),
    defineField({
      name: "metaDescription",
      title: "Meta description",
      type: "text",
      rows: 3,
      group: "seo",
      description: "The search-result snippet, separate from the excerpt. Empty uses the excerpt.",
      validation: (rule) => [
        rule.max(200),
        rule.min(70).warning("Under 70 characters is usually too thin for a snippet."),
        rule.max(160).warning("Over 160 characters may be cut off in search results."),
      ],
    }),
    defineField({
      name: "keywords",
      title: "Keywords",
      type: "array",
      group: "seo",
      of: [defineArrayMember({ type: "string" })],
      options: { layout: "tags" },
      description: "Target search phrases, e.g. interior designers in Kokapet.",
    }),
    defineField({
      name: "publishedAt",
      title: "Published at",
      type: "datetime",
      description: "Posts dated in the future stay hidden until that time (the site checks hourly).",
      initialValue: () => new Date().toISOString(),
      validation: (rule) => rule.required(),
    }),
    defineField({
      name: "author",
      title: "Author",
      type: "reference",
      to: [{ type: "author" }],
      description: 'Empty shows "Atwood Dsigns".',
    }),
    defineField({
      name: "categories",
      title: "Categories",
      type: "array",
      of: [defineArrayMember({ type: "reference", to: [{ type: "category" }] })],
      description: "The first one is the label shown on the card and above the title.",
      validation: (rule) => rule.required().min(1),
    }),
    defineField({
      name: "featured",
      title: "Featured",
      type: "boolean",
      description: "Featured posts are listed first on the Journal page.",
      initialValue: false,
    }),
    defineField({
      name: "coverImage",
      title: "Cover image",
      type: "image",
      description:
        "Shown on Journal cards and in link previews (WhatsApp, Facebook, LinkedIn). Upload at least 1200 × 630 and set the hotspot.",
      options: { hotspot: true },
      validation: (rule) => [rule.required(), minSize(1200, 630)(rule)],
      fields: [altField],
    }),
    defineField({
      name: "heroImage",
      title: "Header image",
      type: "image",
      description:
        "The full-width image behind the title on the post page. Upload at least 1600 px wide. Empty uses the cover image.",
      options: { hotspot: true },
      validation: minSize(1600, 900),
      fields: [altField],
    }),
    defineField({
      name: "readTime",
      title: "Read time (minutes)",
      type: "number",
      description: "Empty works it out from the length of the post.",
      validation: (rule) => rule.min(1).max(60).integer(),
    }),
    defineField({
      name: "body",
      title: "Body",
      type: "blockContent",
      validation: (rule) => rule.required(),
    }),
  ],
  orderings: [
    {
      title: "Newest first",
      name: "publishedAtDesc",
      by: [{ field: "publishedAt", direction: "desc" }],
    },
  ],
  preview: {
    select: {
      title: "title",
      date: "publishedAt",
      featured: "featured",
      media: "coverImage",
    },
    prepare: ({ title, date, featured, media }) => ({
      title,
      subtitle:
        (date ? new Date(date).toLocaleDateString("en-IN") : "Undated") + (featured ? " · Featured" : ""),
      media,
    }),
  },
});
