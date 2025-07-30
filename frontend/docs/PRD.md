# NoaMetrics Landing Page – Lean PRD

> **Document Status:** Draft ⏳  
> **Last Updated:** {{DATE}}

---

## 1. Purpose & Vision
NoaMetrics helps tech companies stop wasting time on unqualified or fraudulent candidates by using AI-powered video analysis and CV fraud detection. The landing page's purpose is to:
1. Clearly communicate the problem (hiring uncertainty & fraud).  
2. Showcase NoaMetrics' solution and forthcoming product.  
3. Drive *early-stage conversion*—collect wait-list sign-ups and demo requests.

## 2. Target Audience
| Persona                | Pain Point                                   | Desired Outcome                       |
|------------------------|----------------------------------------------|---------------------------------------|
| **Startup CTO**        | Fast hiring without mis-hires                | Reliable shortlist in minutes         |
| **Recruiting Manager** | Endless screening calls & CV fraud           | Automated scoring & fraud detection   |
| **Talent Lead**        | Manual interview scheduling & assessment     | AI video analysis with clear insights |

## 3. Problem Statement
> *"Hiring teams spend hours screening hundreds of CVs & calls, yet still risk deepfake interviews and fraudulent candidates."*

## 4. Goals & Success Metrics
| Goal                                   | Metric / KPI                     | Target                  |
|----------------------------------------|----------------------------------|-------------------------|
| Capture qualified leads                | Wait-list sign-ups               | **1 000+ /month**       |
| Encourage demo engagement              | Demo upload interactions         | **25 %** of visitors    |
| Validate messaging & market fit        | Bounce rate, time on page        | < **50 %**, > **1 min** |

## 5. Core Features (MVP)
1. **Hero Section** – Clear headline, value prop, CTA buttons (Wait-list, Free CV analysis).  
2. **Demo Upload Section** – Drag-and-drop area for Job Description & CVs, "Upload" CTA (stubbed).  
3. **Solution Benefits** – Checklist of AI outputs delivered in < 60 s.  
4. **Stats & Social Proof** – Metrics, testimonials, trust badges (future).  
5. **CTA & Footer** – Final conversion push, links, company info.

### User Flow (Happy Path)
```
Visitor opens landing page → Reads hero → Clicks "Analyze Your First 3 CVs Free"
  ↳ Scrolls to Demo Upload → Drags CV/Job file → Clicks Upload
    ↳ "Success" toast (stub) → Wait-list modal → Email submit → Thank-you
```

## 6. Out-of-Scope for MVP
- Payment, account creation, authentication.  
- Multi-language localisation.

## 7. Assumptions & Risks
- Users are willing to share an email in exchange for early access.
- Marketing site must load < 2 s on 3G for global reach.
- Legal & privacy texts will be supplied separately.

## 8. Technical Notes
- **Stack:** Nuxt 3 + Tailwind CSS, TypeScript ready.  
- **SEO:** meta tags, OG data to be added.  
- **Accessibility:** WCAG AA colour contrast, semantic HTML.

## 9. Milestones & Timeline (Indicative)
| Date (T-week) | Deliverable                               |
|---------------|-------------------------------------------|
| T0            | Hero + Video AI section (✔ done)          |
| T+1 week      | Stats, Testimonials, CTA sections         |
| T+2 weeks     | Wait-list form & API integration          |
| T+3 weeks     | SEO / performance optimisation            |
| T+4 weeks     | Launch & marketing campaign               |

## 10. Stakeholders
- **Product Owner:** Founder / Marketing Lead  
- **Design:** Figma screens (v0.3)  
- **Engineering:** Nuxt dev team  
- **Marketing:** Growth & content team

---

*This PRD is intentionally concise—update as the product evolves.* 