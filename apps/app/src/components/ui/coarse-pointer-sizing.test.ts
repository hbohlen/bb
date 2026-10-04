import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import {
  COARSE_POINTER_CHILD_ICON_BUTTON_CLASS,
  COARSE_POINTER_CHECK_SLOT_CLASS,
  COARSE_POINTER_COMPACT_ICON_BUTTON_CLASS,
  COARSE_POINTER_COMPACT_ICON_SIZE_CLASS,
  COARSE_POINTER_COMPACT_ICON_SIZE_SHRINK_CLASS,
  COARSE_POINTER_COMPACT_ROW_HEIGHT_CLASS,
  COARSE_POINTER_DOT_SIZE_CLASS,
  COARSE_POINTER_GLYPH_BOX_CLASS,
  COARSE_POINTER_HEADER_ICON_BUTTON_CLASS,
  COARSE_POINTER_HEADER_REDUCED_GLYPH_ICON_BUTTON_CLASS,
  COARSE_POINTER_ICON_SIZE_CLASS,
  COARSE_POINTER_ICON_SIZE_SHRINK_CLASS,
  COARSE_POINTER_INPUT_HEIGHT_CLASS,
  COARSE_POINTER_PROMPT_ACTION_BUTTON_CLASS,
  COARSE_POINTER_PROMPT_COMBO_BUTTON_CLASS,
  COARSE_POINTER_PROMPT_ICON_ACTION_BUTTON_CLASS,
  COARSE_POINTER_PROVIDER_TAB_SIZE_CLASS,
  COARSE_POINTER_ROW_ACTION_SIZE_CLASS,
  COARSE_POINTER_TOOLBAR_ACTION_BUTTON_CLASS,
} from "@bb/shared-ui/coarse-pointer-sizing";

const MIN_TARGET_PX = 44;
const SPACING_PX = 4;

const here = path.dirname(fileURLToPath(import.meta.url));
const repoFile = (relative: string) =>
  readFileSync(path.resolve(here, relative), "utf8");

const ARBITRARY_PX = /^[hw]-\[(\d+)px\]$/;
const SPACING_UTILITY = /^(?:h|w|size)-(\d+(?:\.\d+)?)$/;

const coarsePixelSize = (utility: string): number => {
  const arbitrary = ARBITRARY_PX.exec(utility);
  if (arbitrary) return Number(arbitrary[1]);
  const spacing = SPACING_UTILITY.exec(utility);
  if (spacing) return Number(spacing[1]) * SPACING_PX;
  throw new Error(`not a size utility: ${utility}`);
};

const coarseSizes = (className: string): string[] =>
  className
    .split(/\s+/)
    .filter((c) => c.startsWith("max-md:pointer-coarse:"))
    .map((c) => c.replace("max-md:pointer-coarse:", ""))
    // Icon-inset variants size the glyph, not the button.
    .filter((c) => !c.includes("[&"))
    // Padding, margin and colour utilities say nothing about the target size.
    .filter((c) => ARBITRARY_PX.test(c) || SPACING_UTILITY.test(c))
    .map(coarsePixelSize);

describe("coarse-pointer sizing floor", () => {
  it("gives every button-shaped constant a coarse size of at least 44px", () => {
    const buttons: Record<string, string> = {
      COARSE_POINTER_HEADER_ICON_BUTTON_CLASS,
      COARSE_POINTER_HEADER_REDUCED_GLYPH_ICON_BUTTON_CLASS,
      COARSE_POINTER_COMPACT_ICON_BUTTON_CLASS,
      COARSE_POINTER_CHILD_ICON_BUTTON_CLASS,
      COARSE_POINTER_TOOLBAR_ACTION_BUTTON_CLASS,
      COARSE_POINTER_PROMPT_ACTION_BUTTON_CLASS,
      COARSE_POINTER_PROMPT_ICON_ACTION_BUTTON_CLASS,
      COARSE_POINTER_PROMPT_COMBO_BUTTON_CLASS,
      COARSE_POINTER_INPUT_HEIGHT_CLASS,
      COARSE_POINTER_COMPACT_ROW_HEIGHT_CLASS,
      COARSE_POINTER_PROVIDER_TAB_SIZE_CLASS,
      COARSE_POINTER_ROW_ACTION_SIZE_CLASS,
    };

    const tooSmall: string[] = [];
    for (const [name, className] of Object.entries(buttons)) {
      for (const px of coarseSizes(className)) {
        if (px < MIN_TARGET_PX) tooSmall.push(`${name} = ${px}px`);
      }
    }

    expect(tooSmall).toEqual([]);
  });

  it("keeps glyph constants at or above 20px on a coarse pointer", () => {
    const glyphs: Record<string, string> = {
      COARSE_POINTER_ICON_SIZE_CLASS,
      COARSE_POINTER_ICON_SIZE_SHRINK_CLASS,
      COARSE_POINTER_COMPACT_ICON_SIZE_CLASS,
      COARSE_POINTER_COMPACT_ICON_SIZE_SHRINK_CLASS,
      COARSE_POINTER_GLYPH_BOX_CLASS,
      COARSE_POINTER_CHECK_SLOT_CLASS,
    };

    const tooSmall: string[] = [];
    for (const [name, className] of Object.entries(glyphs)) {
      for (const px of coarseSizes(className)) {
        if (px < 20) tooSmall.push(`${name} = ${px}px`);
      }
    }

    expect(tooSmall).toEqual([]);
  });

  it("scales the status dot with the pointer but keeps it off the touch floor", () => {
    // A dot is an indicator, not a target. It still has to grow on a coarse
    // pointer to stay visible, so the floor here is legibility rather than the
    // 44px minimum, and the test pins that distinction.
    const coarse = coarseSizes(COARSE_POINTER_DOT_SIZE_CLASS);
    expect(coarse.length).toBeGreaterThan(0);
    for (const px of coarse) {
      expect(px).toBeGreaterThanOrEqual(16);
      expect(px).toBeLessThan(MIN_TARGET_PX);
    }
  });

  it("derives the app's coarse sidebar control size from the 44px token", () => {
    const appCss = repoFile("../../app.css");
    expect(appCss).toContain("--bb-touch-target-min: 44px");
    expect(appCss).toContain(
      "--bb-sidebar-control-size: var(--bb-touch-target-min)",
    );
  });

  it("sets the coarse sidebar row height to 44px", () => {
    const themeCss = repoFile("./theme.css");
    const coarse = /--bb-sidebar-row-height-coarse:\s*([\d.]+)rem;/.exec(themeCss);
    expect(coarse).not.toBeNull();
    expect(Number(coarse![1]) * 16).toBe(MIN_TARGET_PX);
  });
});