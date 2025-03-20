import asyncio
import os
import re
import time
import random
from urllib.parse import urlparse
from playwright.async_api import async_playwright

# Create an output directory for the scraped transcripts
output_dir = "scraped_transcripts"
os.makedirs(output_dir, exist_ok=True)


urls = [
    "https://www.microsoft.com/en-us/worklab/ai-at-work-can-ai-help-with-this",
    "https://www.microsoft.com/en-us/worklab/a-role-model-for-ai-driven-transformation",
    "https://www.microsoft.com/en-us/worklab/llms-are-becoming-a-commodity-now-what",
    "https://www.microsoft.com/en-us/worklab/3-proven-ways-to-make-ai-usage-stick",
    "https://www.microsoft.com/en-us/worklab/the-key-to-a-thriving-workforce-is-a-smart-approach-to-ai",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-what-the-future-workforce-really-cares-about",
    "https://www.microsoft.com/en-us/worklab/11-unexpected-ai-at-work-insights-from-2024",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-what-are-agents-how-do-they-help-businesses",
    "https://www.microsoft.com/en-us/worklab/work-with-ai-like-its-a-colleague-not-a-calculator",
    "https://www.microsoft.com/en-us/worklab/when-it-comes-to-ai-do-not-build-islands-of-intelligence",
    "https://www.microsoft.com/en-us/worklab/with-copilot-every-meeting-is-a-digital-artifact",
    "https://www.microsoft.com/en-us/worklab/the-key-ingredient-in-every-copilot-conversation",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-why-cios-matter-more-than-ever",
    "https://www.microsoft.com/en-us/worklab/inside-ai-native-ad-agency",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-5-copilot-prompts-to-try-out-at-work",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-how-ai-breaks-down-barriers-to-inclusivity",
    "https://www.microsoft.com/en-us/worklab/5-new-habits-will-help-you-get-the-most-out-of-ai-in-2024",
    "https://www.microsoft.com/en-us/worklab/dayana-falcon-espn-talent-mobility-manager-shares-her-moden-work-essentials",
    "https://blogs.microsoft.com/blog/2024/11/12/https-blogs-microsoft-com-blog-2024-11-12-how-real-world-businesses-are-transforming-with-ai/",
    "https://hbr.org/2024/06/how-ai-can-make-make-us-better-leaders",
    "https://www.linkedin.com/pulse/work-ai-like-its-colleague-calculator-jared-spataro-acghc/",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-3-scenarios-for-unlocking-the-full-potential-of-ai",
    "https://www.microsoft.com/en-us/worklab/ai-impact-at-3-industry-leading-companies",
    "https://www.linkedin.com/pulse/when-comes-ai-its-system-model-matters-jared-spataro-l90jc/",
    "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai?cid=soc-web",
    "https://www.microsoft.com/en-us/worklab/ai-a-whole-new-way-of-working",
    "https://www.microsoft.com/en-us/worklab/5-key-principles-for-implementing-an-ai-strategy-across-your-organization",
    "https://www.microsoft.com/en-us/worklab/our-year-with-copilot-what-microsoft-has-learned-about-ai-at-work",
    "https://www.microsoft.com/en-us/worklab/what-we-mean-when-we-say-ai-is-usefully-wrong",
    "https://www.microsoft.com/en-us/worklab/how-ai-gives-you-data-synthesis-superpowers",
    "https://news.microsoft.com/source/wp-content/uploads/2023/11/US51315823-IG-ADA.pdf",
    "https://www.microsoft.com/en-us/worklab/llms-are-becoming-a-commodity-now-what",
    "https://www.microsoft.com/en-us/worklab/the-ripple-effect-of-ai-at-work",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-why-cios-matter-more-than-ever",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-why-cios-matter-more-than-ever",
    "https://www.microsoft.com/en-us/worklab/how-copilot-turns-everyone-into-a-manager",
    "https://www.microsoft.com/en-us/worklab/with-copilot-every-meeting-is-a-digital-artifact",
    "https://www.microsoft.com/en-us/worklab/the-key-ingredient-in-every-copilot-conversation",
    "https://www.microsoft.com/en-us/worklab/the-art-and-science-of-working-with-ai",
    "https://www.microsoft.com/en-us/worklab/why-using-a-polite-tone-with-ai-matters",
    "https://www.microsoft.com/en-us/worklab/what-can-ai-native-startups-teach-the-rest-of-us",
    "https://www.microsoft.com/en-us/worklab/ai-is-already-changing-work-microsoft-included",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-how-ai-breaks-down-barriers-to-inclusivity",
    "https://info.microsoft.com/ww-landing-ai-strategy-roadmap-navigating-the-stages-of-ai-value-creation.html?lcid=EN-US",
    "https://adoption.microsoft.com/en-us/ai-readiness-wizard/",
    "https://www.fastcompany.com/91254572/why-ai-and-skills-are-the-new-barometer-for-organizational-success",
    "https://info.microsoft.com/ww-landing-10-best-practices-to-accelerate-your-employees-ai-skills.html?OCID=cmmerkxrk21",
    "https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RW1jMq4",
    "https://query.prod.cms.rt.microsoft.com/cms/api/am/binary/RW1cZ7v?wt.mc_id=esi_lfo_content_wwl",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-the-11-by-11-tipping-point",
    "https://www.microsoft.com/en-us/worklab/how-i-prompt-leaders-share-their-favorite-ai-time-savers",
    "https://www.microsoft.com/en-us/worklab/how-6-experts-use-next-generation-ai",
    "https://www.microsoft.com/en-us/worklab/when-it-comes-to-ai-do-not-build-islands-of-intelligence",
    "https://www.microsoft.com/en-us/worklab/to-build-ai-into-your-habits-picture-a-pyramid",
    "https://www.linkedin.com/business/talent/blog/learning-and-development/new-framework-for-ai-upskilling?trk=microsoft-li-wti-release",
    "https://www.microsoft.com/en-us/worklab/work-with-ai-like-its-a-colleague-not-a-calculator",
    "https://www.microsoft.com/en-us/worklab/anatomy-of-a-copilot",
    "https://www.microsoft.com/en-us/worklab/3-proven-ways-to-make-ai-usage-stick",
    "https://www.linkedin.com/pulse/can-ai-help-jared-spataro-f5esc/",
    "https://www.microsoft.com/en-us/worklab/enlist-ai-in-your-fight-against-email-overload",
    "https://news.microsoft.com/source/features/ai/6-ai-trends-youll-see-more-of-in-2025/",
    "https://blogs.microsoft.com/blog/2024/11/12/idcs-2024-ai-opportunity-study-top-five-ai-trends-to-watch/",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-in-2025-ai-will-help-us-navigate-uncertainty",
    "https://www.microsoft.com/en-us/worklab/work-trend-index/ai-at-work-is-here-now-comes-the-hard-part",
    "https://business.linkedin.com/content/dam/business/marketing-solutions/global/en_US/site/pdf/infographics/2024-marketing-jobs-outlook.pdf?trk=lms-blog-b2b&src=bl-po",
    "https://business.linkedin.com/talent-solutions/global-talent-trends",
    "https://www.microsoft.com/en-us/worklab/what-new-terms-like-goblin-mode-reveal-about-work-in-2023",
    "https://news.microsoft.com/source/features/innovation/a-conversation-with-kevin-scott-whats-next-in-ai/",
    "https://www.linkedin.com/pulse/why-leaders-cant-ignore-human-energy-crisis-kathleen-hogan/",
    "https://www.linkedin.com/business/talent/blog/learning-and-development/generative-ai-impact-on-learning-and-development",
    "https://www.microsoft.com/en-us/worklab/ai-at-work-in-2025-ai-will-help-us-navigate-uncertainty",
    "https://www.microsoft.com/en-us/worklab/there-are-no-shortcuts-to-high-performance",
    "https://www.microsoft.com/en-us/worklab/how-we-measure-the-value-of-ai-at-work",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-which-jobs-have-an-ai-advantage",
    "https://www.microsoft.com/en-us/worklab/ai-data-drop-what-the-future-workforce-really-cares-about",
    "https://www.washingtonpost.com/washington-post-live/2024/03/28/how-technology-is-transforming-collaboration-innovation-work/",
    "https://msft.it/6049UDDsU",
    "https://www.microsoft.com/en-us/worklab/podcast/microsoft-chief-scientist-on-ai-untapped-potential",
    "https://www.microsoft.com/en-us/worklab/podcast/conor-grennan-on-moving-beyond-the-search-engine-mindset",
    "https://podcast.beyondtheprompt.ai/episodes/practical-strategies-for-leveraging-ai-in-your-business-wharton-professor-ethan-mollick",
    "https://www.microsoft.com/en-us/worklab/podcast/wharton-professor-ethan-mollick-on-the-urgency-of-getting-in-front-of-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/how-ai-can-reveal-the-neural-secrets-behind-great-leadership",
    "https://www.microsoft.com/en-us/worklab/podcast/stanford-professor-erik-brynjolfsson-on-how-ai-will-transform-productivity",
    "https://www.microsoft.com/en-us/worklab/podcast/all-leaders-can-learn-from-how-ai-is-revolutionizing-medicine",
    "https://www.microsoft.com/en-us/worklab/podcast/are-managers-the-key-to-unlocking-the-true-potential-of-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/how-do-you-solve-a-problem-thats-never-been-solved-before",
    "https://www.microsoft.com/en-us/worklab/podcast/how-to-become-an-ai-powered-organization",
    "https://www.microsoft.com/en-us/worklab/podcast/nir-eyal-on-how-to-defeat-distraction-in-an-always-on-world",
    "https://www.microsoft.com/en-us/worklab/podcast/charles-duhigg-on-how-to-build-new-habits-for-the-ai-era",
    "https://www.microsoft.com/en-us/worklab/podcast/eric-horvitz-on-the-possibilities-of-generative-ai-for-human-thriving",
    "https://www.microsoft.com/en-us/worklab/podcast/linkedin-vp-aneesh-raman-on-why-adaptability-is-the-skill-of-the-moment",
    "https://www.microsoft.com/en-us/worklab/podcast/harvard-business-schools-christina-wallace-on-how-ai-can-help-us-rebalance-our-lives",
    "https://www.microsoft.com/en-us/worklab/podcast/microsoft-deputy-cto-sam-schillace-on-how-ai-will-shift-our-productivity-paradigm",
    "https://www.microsoft.com/en-us/worklab/podcast/futurist-amy-webb-on-the-most-plausible-outcomes-for-ai-and-work",
    "https://www.microsoft.com/en-us/worklab/podcast/why-youre-overwhelmed-at-work",
    "https://www.microsoft.com/en-us/worklab/podcast/jenny-lay-flurrie-on-why-inclusivity-benefits-everyone",
    "https://www.microsoft.com/en-us/worklab/podcast/how-leaders-will-use-ai-to-unleash-creativity",
    "https://www.microsoft.com/en-us/worklab/podcast/regain-control-of-your-focus-and-attention-with-researcher-gloria-mark",
    "https://www.microsoft.com/en-us/worklab/podcast/stanford-professor-erik-brynjolfsson-on-how-ai-will-transform-productivity",
    "https://www.microsoft.com/en-us/worklab/podcast/will-ai-make-work-more-human",
    "https://www.microsoft.com/en-us/worklab/podcast/an-ai-first-data-scientist-on-current-limits-and-future-potential-of-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/want-real-ai-transformation-focus-on-people-and-processes",
    "https://www.microsoft.com/en-us/worklab/podcast/tackling-worlds-toughest-problems-with-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/season-5-will-explore-how-to-tap-the-full-potential-of-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/timm-chiusano-on-ai-and-winning-the-week",
    "https://www.microsoft.com/en-us/worklab/podcast/lumen-ceo-kate-johnson-says-leaders-should-be-catalysts",
    "https://www.microsoft.com/en-us/worklab/podcast/charles-lamanna-on-the-next-big-role-for-ai",
    "https://www.microsoft.com/en-us/worklab/podcast/how-can-leaders-invest-the-time-that-ai-gives-back",
    "https://www.goodmorningamerica.com/news/video/microsoft-linkedin-talk-ai-workplace-110018966",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/zi9ic8t9Fk9o7rZyFgssE9",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/AQC5ifDQZ5nHerg7WxQibe",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/qmuNEehwJ9p2UNNwP9AH54",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/d6kVi5ThXLQ4raJui47pob",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/aCiVYwQmXeM5KNSRe4eF1i",
    "https://videos.microsoft.com/infrastructure-for-the-era-of-ai/watch/4xWafUAXA2L8mJGhx6Pbeq",
    "https://www.microsoft.com/en/customers/story/1703814256939529124-volvo-group-automotive-azure-ai-services",
    "https://www.microsoft.com/en-us/worklab/podcast/inside-accentures-ai-journey-with-ceo-julie-sweet",
    "https://www.microsoft.com/en-us/worklab/podcast/how-copilot-is-transforming-one-global-creative-agency",
    "https://www.microsoft.com/en-us/worklab/learn-from-ai-native-firms-or-get-left-behind",
    "https://www.microsoft.com/en-us/worklab/ai-impact-at-dow-copilot-identifies-millions-in-cost-savings",
    "https://techcommunity.microsoft.com/blog/vivasales-blog/how-netlogic-computer-consulting-is-boosting-its-sales-performance-with-microsof/3831750",
    "https://www.microsoft.com/en-us/worklab/how-business-leaders-are-using-copilot-right-now",
    "https://www.microsoft.com/en/customers/story/19404-clifford-chance-microsoft-365-copilot",
    "https://www.microsoft.com/en-us/research/video/at-the-frontiers-of-science-exciting-advances-in-protein-design/",
    "https://www.microsoft.com/en-us/research/blog/ai4science-to-empower-the-fifth-paradigm-of-scientific-discovery/",
    "https://www.microsoft.com/en-us/research/group/ai-for-good-research-lab/",
    "https://www.microsoft.com/en-us/worklab/a-role-model-for-ai-driven-transformation",
    "https://blogs.microsoft.com/blog/2024/10/21/new-autonomous-agents-scale-your-team-like-never-before/",
    "https://news.microsoft.com/source/emea/features/with-copilot-agents-pets-at-home-unleashes-an-ai-revolution/",
    "https://www.microsoft.com/en-us/worklab/dayana-falcon-espn-talent-mobility-manager-shares-her-moden-work-essentials",
    "https://news.microsoft.com/2024/11/14/accenture-microsoft-and-avanade-help-enterprises-reinvent-business-functions-and-industries-with-generative-ai-and-copilot/",
    "https://www.microsoft.com/en-us/microsoft-365/blog/2024/11/19/introducing-copilot-actions-new-agents-and-tools-to-empower-it-teams/",
    "https://customers.microsoft.com/en-us/story/1837247326532243131-canadian-tire-corporation-azure-retailers-en-canada",
    "https://customers.microsoft.com/en-us/story/1837667199713758792-clifford-chance-mcrosoft-365-copilot-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1832762432689198259-dlapiper-microsoft-365-copilot-professional-services-en-united-states",
    "https://customers.microsoft.com/en-us/story/1837633288515694884-eaton-microsoft-365-copilot-discrete-manufacturing-en-united-states",
    "https://customers.microsoft.com/en-us/story/1835026746816257326-harvey-azure-openai-service-other-en-united-states",
    "https://customers.microsoft.com/en-us/story/1838588977497742792-kmslh-azure-openai-service-professional-services-en-israel",
    "https://customers.microsoft.com/en-us/story/1837976425667863739-localiza-microsoft-365-copilot-automotive-en-brazil",
    "https://customers.microsoft.com/en-us/story/1834508996209335697-medigold-health-azure-ai-services-health-provider-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1834023197365666109-pimco-azure-ai-search-banking-and-capital-markets-en-united-states",
    "https://customers.microsoft.com/en-us/story/1833614171187901763-sace-microsoft-viva-suite-insurance-en-italy",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1802756598954587083-access-holdings-plc-microsoft-365-banking-and-capital-markets-en-nigeria&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062272075%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=uXii3vcg4Q3aj7tp7l5VAVbuOyRvmHU3slqCDwqIFjg%3D&reserved=0",
    "https://customers.microsoft.com/en-us/story/1749403583645228440-amadeus-microsoft-365-professional-services-en-france",
    "https://news.microsoft.com/en-au/features/anz-launches-first-of-its-kind-ai-immersion-centre-in-partnership-with-microsoft/",
    "https://customers.microsoft.com/en-us/story/1794442287816192713-asahi-europe-and-international-microsoft-copilot-for-microsoft-365-consumer-goods-en-czechia",
    "https://customers.microsoft.com/en-us/story/1827945851075596388-axon-azure-openai-service-national-government-en-united-states",
    "https://customers.microsoft.com/en-gb/story/1815128464686923048-aztec-group-microsoft-365-copilot-banking-and-capital-markets-en-united-kingdom",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1804968308500747501-sultan-microsoft-copilot-health-provider-en-kuwait&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C7b04ac48f784445af5a008dcf2237a96%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638651481396507436%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=LmqAeVg2CS6IrwfwIOxSztz8qzQxdmpP90z906KtLQQ%3D&reserved=0",
    "https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/10/17/colombia-and-brazil-embrace-the-potential-of-cloud-and-ai-solutions-to-drive-growth-and-tackle-social-challenges/",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1804597267941884304-baptistcare-sharepoint-nonprofit-en-australia&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062359439%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=VDzN%2BADOGokVarGbLEmM4gqpi6OombeQhdYd%2Fo5sT8k%3D&reserved=0",
    "https://ukstories.microsoft.com/features/barnsley-council-releasing-the-potential-with-microsoft-copilot/",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fnews.microsoft.com%2Fsource%2Ffeatures%2Fdigital-transformation%2Fhow-blackrocks-flight-crew-helped-copilot-for-microsoft-365-take-off%2F&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062415337%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=yIbi1evXRe%2BoRXqpF8mcXl7XjRQmrsGGEJn%2FrGAKz4M%3D&reserved=0",
    "https://customers.microsoft.com/en-us/story/1824902121184173261-british-heart-foundation-microsoft-copilot-nonprofit-en-united-kingdom",
    "https://news.microsoft.com/it-it/2024/10/23/microsoft-ceo-satya-nadella-showcases-transformative-power-of-artificial-intelligence-for-italys-growth-at-microsoft-ai-tour-in-rome/?msockid=1033af7595936fd71c19bd9c94546e18",
    "https://customers.microsoft.com/en-us/story/1798374461640442079-capita-group-github-copilot-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1828282129545930288-cdw-corporation-microsoft-viva-learning-consumer-goods-en-united-states",
    "https://news.microsoft.com/source/asia/features/taiwan-hospital-deploys-ai-copilots-to-lighten-workloads-for-doctors-nurses-and-pharmacists/",
    "https://customers.microsoft.com/en-gb/story/1790435165492425096-eon-se-microsoft-copilot-for-microsoft-365-energy-en-germany",
    "https://customers.microsoft.com/en-us/story/1762150085964970175-enerjisa-uretim-microsoft-copilot-energy-en-turkiye",
    "https://customers.microsoft.com/en-us/story/1795477416065405316-epam-systems-microsoft-copilot-for-microsoft-365-professional-services-en-hungary",
    "https://customers.microsoft.com/en-us/story/1826307332667818248-farm-credit-canada-microsoft-365-copilot-government-en-canada",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-us%2Fstory%2F1813696493334607461-finastra-microsoft-copilot-for-microsoft-365-professional-services-en-united-kingdom&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062428568%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=U5kpF%2B3HpIfSYQlB6j47uW5HQ5ELonUZo%2FMO%2FOqsUwI%3D&reserved=0",
    "https://customers.microsoft.com/en-gb/story/1816271784634453515-four-agency-microsoft-365-copilot-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1772353582649569700-ocgoodwill-azure-ai-services-nonprofit-en-united-states",
    "https://www.microsoft.com/en-us/microsoft-365/blog/2024/09/16/microsoft-365-copilot-wave-2-pages-python-in-excel-and-agents/",
    "https://customers.microsoft.com/en-us/story/1821284073143161043-insight-enterprises-inc-surface-laptop-professional-services-en-united-states",
    "https://customers.microsoft.com/en-us/story/1759309014350031747-joos-microsoft-copilot-consumer-goods-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1744468024452864249-kantar-windows-11-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1749522406496386350-kpmg-microsoft-365-copilot-professional-services-en-united-states",
    "https://customers.microsoft.com/en-us/story/1825162116194410361-lgt-excel-banking-and-capital-markets-en-liechtenstein",
    "https://customers.microsoft.com/en-us/story/1804624062321190625-lotte-hotels-and-resorts-azure-ai-studio-travel-and-transportation-en-korea",
    "https://customers.microsoft.com/en-gb/story/1782421038868081701-maire-microsoft-teams-energy-en-italy",
    "https://customers.microsoft.com/en-us/story/1749886282579475320-mcdonalds-china-azure-retailers-en-china",
    "https://customers.microsoft.com/en-us/story/1812248324658189027-mcknight-microsoft-copilot-for-microsoft-365-nonprofit-en-united-states",
    "https://customers.microsoft.com/en-us/story/1759306888687672662-morulahealth-microsoft-365-business-premium-health-provider-en-united-kigdom",
    "https://customers.microsoft.com/en-us/story/1770472924267393932-motor-oil-group-microsoft-365-energy-en-greece",
    "https://customers.microsoft.com/en-us/story/1792966154673709027-nagel-group-azure-openai-service-travel-and-transportation-en-germany",
    "https://customers.microsoft.com/en-us/story/1800598946211744899-nflpa-azure-ai-services-nonprofit-en-united-states",
    "https://customers.microsoft.com/en-us/story/1759188982673652446-o2-microsoft-365-telecommunications-en-czech-republic",
    "https://customers.microsoft.com/en-us/story/1744450394922857891-onepoint-github-copilot-professional-services-en-france",
    "https://customers.microsoft.com/en-us/story/1774095788906881160-orange-azure-openai-service-telecommunications-en-france",
    "https://customers.microsoft.com/en-us/story/1820166640605522715-ouh-microsoft-365-copilot-health-provider-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1790507377097905834-paconsulting-dynamics-365-sales-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1758695276753608190-petrobras-azure-openai-service-energy-en-brazil",
    "https://customers.microsoft.com/en-us/story/1776965075841351020-petrochemical-industries-company-microsoft-365-energy-en-kuwait",
    "https://customers.microsoft.com/en-us/story/1795890438217888078-pkshatech-microsoft-copilot-for-microsoft-365-other-en-japan",
    "https://news.nuance.com/2024-03-08-Providence-and-Microsoft-Enable-AI-Innovation-at-Scale-to-Improve-the-Future-of-Care",
    "https://customers.microsoft.com/en-us/story/1802830664758543360-rti-international-microsoft-teams-nonprofit-en-united-states",
    "https://customers.microsoft.com/en-us/story/1785448033474736158-sandvik-coromant-microsoft-copilot-for-sales-discrete-manufacturing-en-sweden",
    "https://customers.microsoft.com/en-us/story/1735001154382665808-sasfin-bank-azure-banking-en-south-africa",
    "https://customers.microsoft.com/en-us/story/1758915282906956032-scottishwater-microsoft-copilot-energy-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1768027434711024743-shrinerschildrens-azure-health-provider-en-united-states",
    "https://news.microsoft.com/2024/10/24/siemens-and-microsoft-scale-industrial-ai/",
    "https://customers.microsoft.com/en-us/story/1798509188103498351-softchoice-microsoft-copilot-for-microsoft-365-consumer-goods-en-united-states",
    "https://customers.microsoft.com/en-us/story/1823424868741213189-syensqo-azure-open-ai-service-other-en-belgium",
    "https://customers.microsoft.com/en-gb/story/1805001416118108722-teladochealth-power-apps-health-provider-en-united-states",
    "https://customers.microsoft.com/en-us/story/1740058425924206437-telstra-telecommunications-azure-openai-service",
    "https://customers.microsoft.com/en-us/story/1759333055842391656-topsoe-azure-openai-service-discrete-manufacturing-en-denmark",
    "https://customers.microsoft.com/en-us/story/1812576965312816472-torfaen-microsoft-copilot-for-microsoft-365-national-government-en-united-kingdom",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1790119689031635867-trace3-microsoft-365-professional-services-en-united-states&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062303754%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=X4e%2BQhOCohiSCLiVF0no6l2hVQyLM48hr0w7JLmfyhQ%3D&reserved=0",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1802017730982552224-uniper-se-microsoft-copilot-for-microsoft-365-energy-en-germany&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062374306%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=WtghbJqSCe5t36Ng8eihXahtr2MZtlLK3GqOESNFXk8%3D&reserved=0",
    "https://customers.microsoft.com/en-us/story/1772120481217819586-unumgroup-azure-insurance-en-united-states",
    "https://ukstories.microsoft.com/features/how-virgin-atlantic-is-flying-higher-with-copilot/",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1770536569687978092-visier-solutions-azure-openai-service-professional-services-en-canada&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062317741%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=5gKpMYfPtQIxjb4AuR8Axy7XwP5GpD9NT8OGIf3bedY%3D&reserved=0",
    "https://customers.microsoft.com/en-us/story/1828290649088791526-virtualdentalcare-azure-virtual-machines-health-provider-en-united-states",
    "https://customers.microsoft.com/en-us/story/1825622008619351392-zshlavkova-microsoft-365-a3-primary-and-secondary-eduk-12-en-czechia",
    "https://customers.microsoft.com/en-us/story/1836108400811529412-airindia-azure-ai-search-travel-and-transportation-en-india",
    "https://customers.microsoft.com/en-us/story/1832767714677750676-cradle-azure-openai-service-other-unsegmented-en-malaysia",
    "https://customers.microsoft.com/en-us/story/1833973787621467669-doctolib-azure-openai-service-health-provider-en-france",
    "https://customers.microsoft.com/en-us/story/1837822642507786660-docusign-azure-logic-apps-other-en-united-states",
    "https://customers.microsoft.com/en-us/story/1837367358659329204-hollandamerica-microsoft-dataverse-travel-and-transportation-en-united-states",
    "https://customers.microsoft.com/en-us/story/1832880073951334987-jato-dynamics-azure-open-ai-service-automotive-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1838122771592262367-redcross-azure-ai-services-nonprofit-en-kenya",
    "https://customers.microsoft.com/en-us/story/1834923084335117944-laliga-azure-arc-media-and-entertainment-en-spain",
    "https://customers.microsoft.com/en-us/story/1833247205652391288-legrand-cloud-for-manufacturing-discrete-manufacturing-en-france",
    "https://customers.microsoft.com/en-us/story/1835832718338159187-mars-azure-machine-learning-professional-services-en-united-states",
    "https://customers.microsoft.com/en-us/story/1835590701993611997-nba-azure-openai-service-media-and-entertainment-en-united-states",
    "https://customers.microsoft.com/en-us/story/1827391161519296074-orbitalwitness-azure-professional-services-en-united-kingdom",
    "https://customers.microsoft.com/en-us/story/1837624667267994535-parloa-azure-openai-service-professional-services-en-germany",
    "https://customers.microsoft.com/en-us/story/1835402038421112318-zurich-azure-openai-service-insurance-en-switzerland",
    "https://customers.microsoft.com/en-us/story/1783172439597920946-absa-github-copilot-banking-and-capital-markets-en-south-africa",
    "https://customers.microsoft.com/en-us/story/1754582924902623921-adobe-inc-azure-retailers-en-united-states",
    "https://customers.microsoft.com/en-us/story/1749403583645228440-amadeus-microsoft-365-professional-services-en-france",
    "https://news.microsoft.com/en-au/features/anz-launches-first-of-its-kind-ai-immersion-centre-in-partnership-with-microsoft/",
    "https://customers.microsoft.com/en-us/story/1794442287816192713-asahi-europe-and-international-microsoft-copilot-for-microsoft-365-consumer-goods-en-czechia",
    "https://customers.microsoft.com/en-us/story/1760377839901581759-axa-gie-azure-insurance-en-france",
    "https://customers.microsoft.com/en-us/story/1827945851075596388-axon-azure-openai-service-national-government-en-united-states",
    "https://customers.microsoft.com/en-gb/story/1815128464686923048-aztec-group-microsoft-365-copilot-banking-and-capital-markets-en-united-kingdom",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1804968308500747501-sultan-microsoft-copilot-health-provider-en-kuwait&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C7b04ac48f784445af5a008dcf2237a96%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638651481396507436%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=LmqAeVg2CS6IrwfwIOxSztz8qzQxdmpP90z906KtLQQ%3D&reserved=0",
    "https://www.microsoft.com/en-us/microsoft-cloud/blog/2024/10/17/colombia-and-brazil-embrace-the-potential-of-cloud-and-ai-solutions-to-drive-growth-and-tackle-social-challenges/",
    "https://nam06.safelinks.protection.outlook.com/?url=https%3A%2F%2Fcustomers.microsoft.com%2Fen-gb%2Fstory%2F1804597267941884304-baptistcare-sharepoint-nonprofit-en-australia&data=05%7C02%7Ccarissa.eicholz%40microsoft.com%7C234b8aac34a541c47cb308dcde7136e7%7C72f988bf86f141af91ab2d7cd011db47%7C1%7C0%7C638629825062359439%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C0%7C%7C%7C&sdata=VDzN%2BADOGokVarGbLEmM4gqpi6OombeQhdYd%2Fo5sT8k%3D&reserved=0",
    "https://ukstories.microsoft.com/features/barnsley-council-releasing-the-potential-with-microsoft-copilot/"
]

def clean_text(text):
    """Clean and normalize extracted text."""
    text = re.sub(r'\n{2,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def url_to_filename(url):
    """Convert a URL into a clean, safe file name."""
    parsed_url = urlparse(url)
    path = parsed_url.path.strip('/')

    # Get last part of the URL path for the filename
    last_segment = path.split('/')[-1] if path else 'index'

    # Clean: remove query strings, unsafe characters
    safe_filename = re.sub(r'[^\w\-]+', '-', last_segment).strip('-').lower()

    # Add timestamp and random number for uniqueness
    timestamp = int(time.time())
    random_num = random.randint(1000, 9999)
    
    # Append timestamp, random number and .txt extension
    return f"{safe_filename}-{timestamp}-{random_num}.txt"

async def extract_all_paragraphs(page):
    """Extract text from all <p> tags on the page."""
    paragraphs = page.locator("p")
    count = await paragraphs.count()

    if count == 0:
        print("⚠️ No <p> tags found on the page.")
        return ""

    print(f"✅ Found {count} <p> tags on the page. Extracting text...")

    all_paragraphs = []
    for i in range(count):
        text = await paragraphs.nth(i).inner_text()
        if text.strip():
            all_paragraphs.append(text.strip())

    return "\n\n".join(all_paragraphs)

async def scrape_transcript_and_paragraphs(url, page):
    """Visit page, click to show transcript, and extract both transcript and paragraphs."""
    try:
        print(f"\n🔎 Visiting: {url}")

        await page.goto(url, timeout=60000)
        await page.wait_for_load_state('networkidle')

        await asyncio.sleep(2)

        # --- 1. Attempt to click "Show full transcript" ---
        buttons = page.locator("text='Show full transcript'")

        transcript_text = ""
        if await buttons.count() > 0:
            print("✅ Found and clicking 'Show full transcript' button.")
            await buttons.first.click()
            await asyncio.sleep(2)

            # Look for transcript container after clicking
            transcript_selector_candidates = [
                "div[aria-label='Transcript']",
                "div.transcript",
                "div[class*='transcript']",
                "div[aria-labelledby*='Transcript']"
            ]

            for selector in transcript_selector_candidates:
                transcript_section = page.locator(selector)
                if await transcript_section.count() > 0:
                    print(f"✅ Found transcript container: {selector}")
                    transcript_text = await transcript_section.first.inner_text()
                    break

            if not transcript_text:
                print("⚠️ Clicked button, but no transcript container found.")

        # --- 2. Always extract all <p> tags, regardless of transcript presence ---
        page_paragraphs_text = await extract_all_paragraphs(page)

        # Clean text outputs
        transcript_text = clean_text(transcript_text) if transcript_text else "No transcript found."
        page_paragraphs_text = clean_text(page_paragraphs_text) if page_paragraphs_text else "No paragraphs found."

        return transcript_text, page_paragraphs_text

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return "", ""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for url in urls:
            transcript_text, page_paragraphs_text = await scrape_transcript_and_paragraphs(url, page)

            filename = url_to_filename(url)
            filepath = os.path.join(output_dir, filename)

            # --- Combine both contents into one file ---
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"URL: {url}\n\n")

                f.write("=== TRANSCRIPT CONTENT ===\n\n")
                f.write(transcript_text + "\n\n")

                f.write("=== PAGE PARAGRAPHS CONTENT ===\n\n")
                f.write(page_paragraphs_text)

            print(f"💾 Saved combined transcript and paragraphs to {filepath}")

        await browser.close()

    print("\n✅ Done scraping all URLs.")

if __name__ == "__main__":
    asyncio.run(main())