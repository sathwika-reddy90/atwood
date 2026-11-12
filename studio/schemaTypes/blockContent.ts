import { defineArrayMember, defineField, defineType } from "sanity";

import { youtubeId } from "../youtube";

/**
 * Rich text for post bodies. Kept to what the Journal template renders — every
 * style and block here has a case in `render_body()` in tools/cms.py,
 * so an author can't produce a layout the site has no answer for.
 *
 * There is deliberately no H1: the post title is the page's one H1, so the
 * body starts at H2.
 */
export const blockContent = defineType({
  name: "blockContent",
  title: "Body",
  type: "array",
  of: [
    defineArrayMember({
      type: "block",
      styles: [
        { title: "Paragraph", value: "normal" },
        { title: "Heading (H2)", value: "h2" },
        { title: "Subheading (H3)", value: "h3" },
        { title: "Minor heading (H4)", value: "h4" },
        { title: "Quote", value: "blockquote" },
      ],
      lists: [
        { title: "Bullets", value: "bullet" },
        { title: "Numbered", value: "number" },
      ],
      marks: {
        decorators: [
          { title: "Bold", value: "strong" },
          { title: "Italic", value: "em" },
        ],
        annotations: [
          defineArrayMember({
            name: "link",
            title: "Link",
            type: "object",
            fields: [
              defineField({
                name: "href",
                title: "URL",
                type: "url",
                validation: (rule) =>
                  rule.uri({
                    allowRelative: true,
                    scheme: ["http", "https", "mailto", "tel"],
                  }),
              }),
            ],
          }),
        ],
      },
    }),
    defineArrayMember({
      type: "image",
      options: { hotspot: true },
      fields: [
        defineField({
          name: "alt",
          title: "Alt text",
          type: "string",
          description: "Describe the image for screen readers.",
          validation: (rule) => rule.required(),
        }),
        defineField({ name: "caption", title: "Caption", type: "string" }),
      ],
    }),
    defineArrayMember({
      name: "highlight",
      title: "Highlight box",
      type: "object",
      description: "A shaded box for a key takeaway or tip.",
      fields: [
        defineField({ name: "title", title: "Heading", type: "string" }),
        defineField({
          name: "body",
          title: "Text",
          type: "text",
          rows: 4,
          validation: (rule) => rule.required(),
        }),
      ],
      preview: {
        select: { title: "title", subtitle: "body" },
        prepare: ({ title, subtitle }) => ({
          title: `Highlight · ${title || "Key point"}`,
          subtitle,
        }),
      },
    }),
    defineArrayMember({
      name: "youtube",
      title: "YouTube video",
      type: "object",
      fields: [
        defineField({
          name: "url",
          title: "YouTube URL",
          type: "url",
          description: "e.g. https://www.youtube.com/watch?v=Vb8vSnIsPqI",
          validation: (rule) =>
            rule.required().custom((url?: string) =>
              !url || youtubeId(url) ? true : "That doesn't look like a YouTube video link.",
            ),
        }),
        defineField({
          name: "title",
          title: "Video title",
          type: "string",
          description: "Read out by screen readers and shown as the caption.",
          validation: (rule) => rule.required(),
        }),
      ],
      preview: {
        select: { title: "title", subtitle: "url" },
        prepare: ({ title, subtitle }) => ({
          title: title ? `Video · ${title}` : "Video",
          subtitle,
        }),
      },
    }),
    defineArrayMember({
      name: "table",
      title: "Table",
      type: "object",
      fields: [
        defineField({
          name: "caption",
          title: "Caption",
          type: "string",
          description: "Optional. Says what the table compares.",
        }),
        defineField({
          name: "headerRow",
          title: "First row is the header",
          type: "boolean",
          initialValue: true,
        }),
        defineField({
          name: "rows",
          title: "Rows",
          type: "array",
          of: [
            defineArrayMember({
              name: "tableRow",
              title: "Row",
              type: "object",
              fields: [
                defineField({
                  name: "cells",
                  title: "Cells",
                  type: "array",
                  of: [defineArrayMember({ type: "string" })],
                  validation: (rule) => rule.required().min(1),
                }),
              ],
              preview: {
                select: { cells: "cells" },
                prepare: ({ cells }: { cells?: string[] }) => ({
                  title: (cells ?? []).join("  |  ") || "Empty row",
                }),
              },
            }),
          ],
          validation: (rule) => [
            rule.required().min(1),
            rule
              .custom((rows?: { cells?: string[] }[]) => {
                const widths = new Set((rows ?? []).map((r) => r.cells?.length ?? 0));
                return widths.size <= 1 || "Every row should have the same number of cells.";
              })
              .warning(),
          ],
        }),
      ],
      preview: {
        select: { caption: "caption", rows: "rows" },
        prepare: ({ caption, rows }: { caption?: string; rows?: { cells?: string[] }[] }) => ({
          title: caption || "Table",
          subtitle: `${rows?.length ?? 0} rows · ${(rows?.[0]?.cells ?? []).join(", ")}`,
        }),
      },
    }),
    defineArrayMember({
      name: "faq",
      title: "FAQ",
      type: "object",
      fields: [
        defineField({
          name: "title",
          title: "Section heading",
          type: "string",
          initialValue: "Frequently asked questions",
          description: "Rendered as an H2. Each question below becomes an H3.",
        }),
        defineField({
          name: "items",
          title: "Questions",
          type: "array",
          of: [
            defineArrayMember({
              name: "faqItem",
              title: "Question",
              type: "object",
              fields: [
                defineField({
                  name: "question",
                  title: "Question",
                  type: "string",
                  validation: (rule) => rule.required(),
                }),
                defineField({
                  name: "answer",
                  title: "Answer",
                  type: "text",
                  rows: 4,
                  validation: (rule) => rule.required(),
                }),
              ],
              preview: { select: { title: "question", subtitle: "answer" } },
            }),
          ],
          validation: (rule) => rule.required().min(1),
        }),
      ],
      preview: {
        select: { title: "title", items: "items" },
        prepare: ({ title, items }: { title?: string; items?: unknown[] }) => ({
          title: title || "FAQ",
          subtitle: `FAQ · ${items?.length ?? 0} questions`,
        }),
      },
    }),
    defineArrayMember({
      name: "cta",
      title: "CTA button",
      type: "object",
      fields: [
        defineField({
          name: "text",
          title: "Button text",
          type: "string",
          description: "e.g. Book a consultation, See the portfolio",
          validation: (rule) => rule.required().max(40),
        }),
        defineField({
          name: "url",
          title: "Button URL",
          type: "url",
          description: "A site page like contact.html, or a full https:// address.",
          validation: (rule) =>
            rule.required().uri({
              allowRelative: true,
              scheme: ["http", "https", "mailto", "tel"],
            }),
        }),
        defineField({
          name: "newTab",
          title: "Open in new tab",
          type: "boolean",
          initialValue: false,
        }),
      ],
      preview: {
        select: { title: "text", subtitle: "url" },
        prepare: ({ title, subtitle }: { title?: string; subtitle?: string }) => ({
          title: title ? `Button · ${title}` : "Button",
          subtitle,
        }),
      },
    }),
  ],
});
