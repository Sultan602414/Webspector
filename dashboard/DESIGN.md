```markdown
# Design System Document: Cinematic Precision

## 1. Overview & Creative North Star
This design system is built to transcend the utility-heavy nature of QA tools, transforming technical data into a premium, editorial experience. 

**Creative North Star: "The Ethereal Observer"**
The system is designed to feel like a high-end lens—precise, transparent, and sophisticated. We move away from the "standard SaaS dashboard" by rejecting rigid grid lines and high-contrast borders. Instead, we utilize **Tonal Depth** and **Asymmetrical Breathing Room**. The interface should feel less like a software application and more like a curated command center, where AI insights are surfaced through layers of light and shadow rather than boxes and lines.

---

1.  ## 2. Colors: The Depth of Shadow
The palette is rooted in a deep, nocturnal spectrum. We use color not just for decoration, but to define the physical architecture of the interface.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section off content. In this design system, boundaries are defined exclusively through background color shifts. A section is born where a `surface-container-low` block meets a `surface` background. This creates a seamless, "molded" look that feels expensive and intentional.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the Surface tiers to create a logical "lift":
- **Base Level:** `background` (#0b1326) – The infinite canvas.
- **Sectioning:** `surface-container-low` (#131b2e) – Large structural areas.
- **Interactive/Content Blocks:** `surface-container` (#171f33) – The primary container for cards and modules.
- **Focus Elements:** `surface-container-high` (#222a3d) – Elements that require immediate attention or hover states.

### The "Glass & Gradient" Rule
Standard flat colors lack the "soul" required for a premium AI tool. 
- **Signature Textures:** For primary actions, use a linear gradient from `primary` (#c0c1ff) to `secondary` (#d0bcff). 
- **Glassmorphism:** Floating elements (modals, dropdowns, tooltips) should use semi-transparent `surface-bright` with a `backdrop-blur` of 12px to 20px. This allows the vibrant navy background to bleed through, softening the interface.

---

## 3. Typography: Editorial Authority
We use **Inter** as our typographic backbone, leaning into its clean, technical heritage. The hierarchy is designed for "Scan-ability" and "Authority."

- **Display Scales:** Use `display-lg` and `display-md` sparingly for hero metrics or high-level AI summaries. These should have a slight letter-spacing of `-0.02em` to feel tighter and more "designed."
- **Contrast as Hierarchy:** Pair a `headline-sm` title with a `label-md` uppercase subtitle. The extreme difference in size and weight creates an editorial feel found in luxury magazines.
- **Body Text:** Use `body-md` for general legibility. Ensure line-height is generous (1.6) to maintain the "Spacious" requirement of the system.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are often "dirty." In this system, we achieve elevation through light and translucency.

- **The Layering Principle:** Stack your containers. For example, place a `surface-container-lowest` card inside a `surface-container-low` section. This creates a "recessed" or "sunken" look that adds tactile depth without visual clutter.
- **Ambient Shadows:** When an element must float (like a Command Palette), use a shadow with a 40px–60px blur and only 6% opacity. The shadow color must be tinted with our `primary` Indigo—never pure black—to simulate natural light passing through blue glass.
- **The "Ghost Border" Fallback:** If a layout absolutely requires a border for accessibility, use the `outline-variant` (#464554) at **15% opacity**. It should be a suggestion of a line, not a boundary.

---

## 5. Components: The Primitive Set

### Buttons
- **Primary:** Gradient background (`primary` to `secondary`). `lg` (1rem) rounded corners. Use `on_primary` for text to ensure high-contrast legibility.
- **Secondary:** Transparent background with a `Ghost Border`. Text set to `primary`.
- **Tertiary/Ghost:** No background or border. Text set to `on_surface_variant`. 

### Input Fields
- **Style:** Background set to `surface_container_highest`. No border. Bottom-only focus indicator using a 2px `primary` gradient.
- **States:** On error, use `error` (#ffb4ab) text and a subtle `error_container` glow behind the input.

### Cards & Lists
- **Rule:** **No Divider Lines.** To separate list items, use a 4px vertical gap and alternate subtle background shifts, or simply use the Spacing Scale to let white space do the work.
- **AI Highlight Cards:** Use a `surface-container-highest` background with a subtle 1px inner glow (top-left) using `primary` at 10% opacity.

### Chips & Badges
- **QA Status:** Use `tertiary` (#89ceff) for "In Progress" and `secondary` for "Complete." Chips should be pill-shaped (`full` roundedness) and use a low-opacity version of the color as a background.

---

## 6. Do’s and Don’ts

### Do
- **Do** prioritize "Dark Space." If a layout feels cramped, increase the padding to 32px or 48px. 
- **Do** use thin (1.5pt) line icons to match the sophistication of the typography.
- **Do** use intentional asymmetry. Align a headline to the left but place the supporting AI data in a floating glass card offset to the right.

### Don't
- **Don't** use pure black (#000000). It kills the depth of the navy-charcoal atmosphere.
- **Don't** use 90-degree corners. Everything must feel approachable yet engineered (12px–16px radius).
- **Don't** use high-contrast dividers. If you feel the need to "split" the screen, use a background color change from `surface` to `surface-container-low`.

---

**Director’s Final Note:** 
This design system is about the *absence* of noise. Every element should feel like it was placed with a purpose. When in doubt, take a line away and add a layer of depth instead. Focus on the light.```