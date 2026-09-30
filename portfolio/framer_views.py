import os
import re
import json
from django.http import HttpResponse, Http404
from django.conf import settings
from .models import Project, BlogPost, SiteSettings, Category, Service, Testimonial, FAQ

FRAMER_DIR = os.path.join(settings.BASE_DIR, "portavia.framer.website")


def _inject_dynamic_data(html, context_type="general", item_slug=None):
    """
    Keeps 100% of original Framer HTML, CSS, Motion scripts, and 3D animations intact.
    Injects updated content and backend dashboard link without altering any UI.
    Supports real-time editing and deletion of projects, blogs, services, testimonials, FAQs, and settings.
    """
    site_settings = SiteSettings.get_solo()
    active_projects = list(Project.objects.all())
    active_services = list(Service.objects.filter(is_active=True))
    active_testimonials = list(Testimonial.objects.filter(is_active=True))
    active_faqs = list(FAQ.objects.filter(is_active=True))
    active_blogs = list(BlogPost.objects.filter(is_published=True))

    payload = {
        "designer_name": site_settings.designer_name or "Duncan Robert",
        "hero_role_1": site_settings.hero_role_1 or "DIGITAL",
        "hero_role_2": site_settings.hero_role_2 or "DESIGNER",
        "hero_subheadline": site_settings.hero_subheadline or "",
        "about_text": site_settings.about_text or site_settings.bio or "",
        "avatar_url": site_settings.avatar_image.url if site_settings.avatar_image else "",
        "services_image_url": site_settings.services_image.url if site_settings.services_image else "",
        "stat_experience_num": site_settings.stat_experience_num or "6+",
        "stat_experience_label": site_settings.stat_experience_label or "Years of Experience",
        "stat_projects_num": site_settings.stat_projects_num or "50+",
        "stat_projects_label": site_settings.stat_projects_label or "Completed Projects",
        "stat_clients_num": site_settings.stat_clients_num or "30+",
        "stat_clients_label": site_settings.stat_clients_label or "Clients on Worldwide",
        "stat_satisfaction_num": site_settings.stat_satisfaction_num or "99%",
        "stat_satisfaction_label": site_settings.stat_satisfaction_label or "Satisfaction Rate",
        "stat_growth_num": site_settings.stat_growth_num or "200%",
        "stat_growth_label": site_settings.stat_growth_label or "Growth",
        "services_subtitle": site_settings.services_subtitle or "",
        "projects_subtitle": site_settings.projects_subtitle or "",
        "testimonials_subtitle": site_settings.testimonials_subtitle or "",
        "faq_subtitle": site_settings.faq_subtitle or "",
        "blogs_subtitle": site_settings.blogs_subtitle or "",
        "phone": site_settings.phone or "",
        "email": site_settings.email or "",
        "location": site_settings.location or "",
        "availability": site_settings.availability_status or "",
        "copyright": site_settings.copyright_text or "",
        "dribbble": site_settings.dribbble_url or "",
        "behance": site_settings.behance_url or "",
        "twitter": site_settings.twitter_url or "",
        "instagram": site_settings.instagram_url or "",
        "projects": [
            {
                "id": p.id,
                "slug": p.slug,
                "title": p.title,
                "category": p.category.name if p.category else "Design",
                "cover_url": p.cover_url,
                "tagline": p.tagline or p.short_description
            }
            for p in active_projects
        ],
        "services": [
            {
                "id": s.id,
                "order_num": s.order_num,
                "title": s.title,
                "description": s.description
            }
            for s in active_services
        ],
        "testimonials": [
            {
                "id": t.id,
                "client_name": t.client_name,
                "client_role": t.client_role,
                "client_company": t.client_company,
                "quote": t.quote,
                "avatar_url": t.avatar_url
            }
            for t in active_testimonials
        ],
        "faqs": [
            {
                "id": f.id,
                "order_num": f.order_num,
                "question": f.question,
                "answer": f.answer
            }
            for f in active_faqs
        ],
        "blogs": [
            {
                "id": b.id,
                "slug": b.slug,
                "title": b.title,
                "category": b.category.name if b.category else "Insights",
                "date": b.published_date.strftime("%b %d, %Y") if b.published_date else "",
                "cover_url": b.cover_url,
                "summary": b.summary
            }
            for b in active_blogs
        ]
    }
    payload_json = json.dumps(payload)

    # 2. Inject Smart Client-Side Synchronizer
    sync_script_template = '''
    <style id="framer-django-layout-fixes">
    /* 1. Prevent Hero clipping: Ensure left title word and designer name are never cut off */
    .framer-bmwyn, .framer-14gfby1, .framer-bo4nxh, .framer-iesngu {
        overflow: visible !important;
    }
    .framer-su46cm {
        overflow: visible !important;
        position: relative !important;
    }

    /* 2. Desktop Hero Positioning: Perfect alignment and flow without overlap or horizontal overflow */
    @media (min-width: 1200px) {
        .framer-eownb9 {
            overflow: visible !important;
            position: absolute !important;
            top: -42px !important;
            left: 4px !important;
            width: auto !important;
            max-width: 450px !important;
            white-space: nowrap !important;
            z-index: 20 !important;
        }
        .framer-ba1bwc {
            display: flex !important;
            flex-direction: column !important;
            align-items: flex-start !important;
            justify-content: center !important;
            overflow: visible !important;
            position: relative !important;
            width: auto !important;
        }
        .framer-1behxzj {
            position: relative !important;
            top: auto !important;
            bottom: auto !important;
            left: auto !important;
            right: auto !important;
            margin-top: 16px !important;
            width: 100% !important;
            max-width: 320px !important;
            overflow: visible !important;
            z-index: 10 !important;
        }
        .framer-q5jzto p {
            font-size: 13.5px !important;
            line-height: 1.5 !important;
            text-align: right !important;
        }
    }

    /* 3. Mobile / Tablet Hero Positioning: Clean centered stack */
    @media (max-width: 1199px) {
        .framer-iesngu {
            padding-top: 70px !important;
        }
        .framer-su46cm {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }
        .framer-eownb9 {
            position: relative !important;
            top: 0 !important;
            left: 0 !important;
            margin-bottom: 6px !important;
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
            z-index: 20 !important;
        }
        .framer-ba1bwc {
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            overflow: visible !important;
            position: relative !important;
        }
        .framer-1behxzj {
            position: relative !important;
            top: auto !important;
            bottom: auto !important;
            left: auto !important;
            right: auto !important;
            margin-top: 14px !important;
            width: 100% !important;
            max-width: 340px !important;
        }
        .framer-q5jzto p {
            font-size: 13.5px !important;
            line-height: 1.5 !important;
            text-align: center !important;
        }
    }

    .framer-r8sngb p {
        font-size: 15px !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }

    /* 4. Auto-fit hero title words: Prevent long words from breaking container */
    .framer-t476v9, .framer-h6ciaq {
        overflow: visible !important;
        width: auto !important;
    }
    .framer-t476v9 h1, .framer-h6ciaq h1 {
        overflow: visible !important;
        white-space: nowrap !important;
        line-height: 0.95 !important;
    }

    /* 5. Completely remove Framer promo banners, template buttons, and badges */
    #__framer-badge-container,
    [data-framer-name*="you can delete"],
    [name*="you can delete"],
    [data-framer-name*="Get Template"],
    [data-framer-name*="New Release"],
    .framer-rcd755-container,
    .framer-1fin31n-container,
    #backend-admin-badge {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    </style>

    <script id="framer-django-live-sync">
    (function() {
        var DATA = __PAYLOAD_JSON__;
        var isSyncing = false;
        var observerActive = true;
        var obs = null;
        var debounceTimer = null;

        function calcWordFontSize(word) {
            var len = (word || "").trim().length;
            if (len <= 7) return "120px";
            if (len <= 9) return "96px";
            if (len <= 11) return "74px";
            if (len <= 13) return "60px";
            return "48px";
        }

        function syncContent() {
            if (isSyncing) return;
            isSyncing = true;
            if (obs) obs.disconnect();

            try {
                // -1. Remove Framer promo widgets & badges from DOM
                document.querySelectorAll('#__framer-badge-container, [data-framer-name*="you can delete"], [name*="you can delete"], [data-framer-name*="Get Template"], [data-framer-name*="New Release"], .framer-rcd755-container, .framer-1fin31n-container, #backend-admin-badge').forEach(function(el) {
                    el.remove();
                });

                // 0. Direct Element Selectors with Auto-Scaling Font
                if (DATA.designer_name) {
                    document.querySelectorAll('.framer-r8sngb p').forEach(function(el) {
                        if (el.textContent.trim() !== DATA.designer_name) {
                            el.textContent = DATA.designer_name;
                        }
                    });
                }

                // Dynamic font scaling for Word 1 based on character count:
                var w1 = (DATA.hero_role_1 || "DIGITAL").trim();
                var fs1 = calcWordFontSize(w1);
                document.querySelectorAll('.framer-t476v9 h1').forEach(function(el) {
                    if (el.textContent.trim() !== w1) {
                        el.textContent = w1;
                    }
                    el.style.setProperty("font-size", fs1, "important");
                    el.style.setProperty("line-height", "0.95", "important");
                });

                // Dynamic font scaling for Word 2 based on character count:
                var w2 = (DATA.hero_role_2 || "DESIGNER").trim();
                var fs2 = calcWordFontSize(w2);
                document.querySelectorAll('.framer-h6ciaq h1').forEach(function(el) {
                    if (el.textContent.trim() !== w2) {
                        el.textContent = w2;
                    }
                    el.style.setProperty("font-size", fs2, "important");
                    el.style.setProperty("line-height", "0.95", "important");
                });

                if (DATA.hero_subheadline) {
                    document.querySelectorAll('.framer-q5jzto p').forEach(function(el) {
                        if (el.textContent.trim() !== DATA.hero_subheadline) {
                            el.textContent = DATA.hero_subheadline;
                        }
                    });
                }

                if (DATA.about_text) {
                    document.querySelectorAll('.framer-13sexmm p').forEach(function(el) {
                        if (el.textContent.trim() !== DATA.about_text) {
                            el.textContent = DATA.about_text;
                        }
                    });
                }

                if (DATA.services_subtitle) {
                    document.querySelectorAll('.framer-dhjg6f p').forEach(function(el) {
                        if (el.textContent.trim() !== DATA.services_subtitle) {
                            el.textContent = DATA.services_subtitle;
                        }
                    });
                }

                if (DATA.faq_subtitle) {
                    document.querySelectorAll('.framer-9bmrrp p').forEach(function(el) {
                        if (el.textContent.trim() !== DATA.faq_subtitle) {
                            el.textContent = DATA.faq_subtitle;
                        }
                    });
                }

                // 1. Phone & Email links
                if (DATA.phone) {
                    document.querySelectorAll('a[href*="tel:"]').forEach(function(a) {
                        var targetHref = "tel:" + DATA.phone.replace(/[^0-9+]/g, "");
                        if (a.href !== targetHref) a.href = targetHref;
                        if (a.textContent.trim() !== DATA.phone) a.textContent = DATA.phone;
                    });
                }

                if (DATA.email) {
                    document.querySelectorAll('a[href*="mailto:"]').forEach(function(a) {
                        var targetHref = "mailto:" + DATA.email;
                        if (a.href !== targetHref) a.href = targetHref;
                        if ((a.textContent.indexOf("@") !== -1 || a.textContent.indexOf("designer") !== -1) && a.textContent.trim() !== DATA.email) {
                            a.textContent = DATA.email;
                        }
                    });
                }

                // 2. Interactive 3D Hero Card Images (Front & Back)
                var frontImgUrl = DATA.avatar_url;
                var backImgUrl = DATA.services_image_url || DATA.avatar_url;

                if (frontImgUrl) {
                    // Central Hero Portrait (Front View: qrxY8NagVO40NBrdhFEGgFR3PYY)
                    document.querySelectorAll('img[src*="qrxY8NagVO40NBrdhFEGgFR3PYY"], img[srcset*="qrxY8NagVO40NBrdhFEGgFR3PYY"]').forEach(function(img) {
                        img.removeAttribute('srcset');
                        img.removeAttribute('sizes');
                        if (img.src !== frontImgUrl) {
                            img.src = frontImgUrl;
                        }
                    });

                    // Floating Navbar circular avatar (IUYreEo8ON7qCLgK2tgDOW0xoI)
                    document.querySelectorAll('img[src*="IUYreEo8ON7qCLgK2tgDOW0xoI"], img[srcset*="IUYreEo8ON7qCLgK2tgDOW0xoI"]').forEach(function(img) {
                        img.removeAttribute('srcset');
                        img.removeAttribute('sizes');
                        if (img.src !== frontImgUrl) {
                            img.src = frontImgUrl;
                        }
                    });
                }

                if (backImgUrl) {
                    // 3D Card Back View / Drag flip animation / Services Card (VRQgkdWsjawSg1qpCm45HfSY1I)
                    document.querySelectorAll('img[src*="VRQgkdWsjawSg1qpCm45HfSY1I"], img[srcset*="VRQgkdWsjawSg1qpCm45HfSY1I"]').forEach(function(img) {
                        img.removeAttribute('srcset');
                        img.removeAttribute('sizes');
                        if (img.src !== backImgUrl) {
                            img.src = backImgUrl;
                        }
                    });
                }

                // 3. Projects Sync (Edit & Deletion)
                var activeProjectSlugs = {};
                DATA.projects.forEach(function(p) { activeProjectSlugs[p.slug] = p; });

                document.querySelectorAll('a[href*="projects/"]').forEach(function(a) {
                    var href = a.getAttribute("href") || "";
                    var match = href.match(/projects\/([^\/\.]+)/);
                    if (match && match[1]) {
                        var slug = match[1];
                        var card = a.closest('[data-framer-name="Card"], [data-framer-name*="Project"], .framer-1') || a;

                        if (!activeProjectSlugs[slug]) {
                            // Deleted in dashboard -> Hide from UI
                            if (card.style.display !== "none") card.style.display = "none";
                        } else {
                            var proj = activeProjectSlugs[slug];
                            if (card.style.display === "none") card.style.display = "";
                            var h = card.querySelector('h2, h3, [data-framer-name="Title"]');
                            if (h && proj.title && h.textContent.trim() !== proj.title) {
                                h.textContent = proj.title;
                            }
                        }
                    }
                });

                // 4. Blogs Sync (Edit & Deletion)
                var activeBlogSlugs = {};
                DATA.blogs.forEach(function(b) { activeBlogSlugs[b.slug] = b; });

                document.querySelectorAll('a[href*="blogs/"]').forEach(function(a) {
                    var href = a.getAttribute("href") || "";
                    var match = href.match(/blogs\/([^\/\.]+)/);
                    if (match && match[1]) {
                        var slug = match[1];
                        var card = a.closest('[data-framer-name="Card"], [data-framer-name*="Blog"], .framer-1') || a;

                        if (!activeBlogSlugs[slug]) {
                            // Deleted in dashboard -> Hide from UI
                            if (card.style.display !== "none") card.style.display = "none";
                        } else {
                            var blog = activeBlogSlugs[slug];
                            if (card.style.display === "none") card.style.display = "";
                            var h = card.querySelector('h2, h3, [data-framer-name="Title"]');
                            if (h && blog.title && h.textContent.trim() !== blog.title) {
                                h.textContent = blog.title;
                            }
                        }
                    }
                });

                // 5. Testimonials Sync (Edit & Deletion)
                var activeTestimonialNames = {};
                DATA.testimonials.forEach(function(t) { activeTestimonialNames[t.client_name.toLowerCase()] = t; });

                var defaultNames = ["john harris", "michael lee", "sarah johnson", "laura bennett"];
                defaultNames.forEach(function(defName) {
                    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    var node;
                    while (node = walker.nextNode()) {
                        if (node.nodeValue && node.nodeValue.toLowerCase().indexOf(defName) !== -1) {
                            var card = node.parentElement ? node.parentElement.closest('[data-framer-name="Card"], .framer-1, div[style*="border"]') : null;
                            if (!card && node.parentElement) card = node.parentElement.parentElement;
                            
                            var tData = activeTestimonialNames[defName];
                            if (!tData && card) {
                                // Testimonial was deleted in dashboard -> Hide from UI
                                if (card.style.display !== "none") card.style.display = "none";
                            } else if (tData && card) {
                                if (card.style.display === "none") card.style.display = "";
                                if (node.nodeValue !== tData.client_name) {
                                    node.nodeValue = tData.client_name;
                                }
                            }
                            break;
                        }
                    }
                });

                // 5.5. Services Accordion Sync (Titles, Bullets, Subtitle)
                if (DATA.services_subtitle) {
                    document.querySelectorAll('#service .framer-dhjg6f p, #service p').forEach(function(p) {
                        if (p.textContent.indexOf('As a digital designer') !== -1 || p.textContent.indexOf('visual storyteller') !== -1) {
                            if (p.textContent.trim() !== DATA.services_subtitle) {
                                p.textContent = DATA.services_subtitle;
                            }
                        }
                    });
                }

                if (DATA.services && DATA.services.length > 0) {
                    var serviceBoxes = document.querySelectorAll('#service .framer-Oq4zO');
                    DATA.services.forEach(function(s, idx) {
                        if (idx < serviceBoxes.length) {
                            var box = serviceBoxes[idx];
                            if (box.style.display === "none") box.style.display = "";

                            // Update Header Title (e.g. "1. UI/UX DESIGN")
                            var h3 = box.querySelector('h3');
                            var fullTitle = (s.order_num ? s.order_num.trim() + " " : "") + s.title.trim();
                            if (h3 && h3.textContent.trim().toLowerCase() !== fullTitle.toLowerCase()) {
                                h3.textContent = fullTitle;
                            }

                            // Update Description Bullets
                            if (s.description) {
                                var rawLines = s.description.split(String.fromCharCode(10));
                                var bullets = [];
                                for (var li = 0; li < rawLines.length; li++) {
                                    var line = rawLines[li].replace(new RegExp(String.fromCharCode(13), "g"), "").replace(/^[-•*]\s*/, "").trim();
                                    if (line) bullets.push(line);
                                }

                                if (bullets.length === 1 && bullets[0].indexOf(".") !== -1) {
                                    var dotSplit = bullets[0].split(".");
                                    var cleanDots = [];
                                    for (var di = 0; di < dotSplit.length; di++) {
                                        var dItem = dotSplit[di].trim();
                                        if (dItem) cleanDots.push(dItem);
                                    }
                                    if (cleanDots.length > 1) bullets = cleanDots;
                                }

                                var bulletPs = box.querySelectorAll('.framer-188sluc p');
                                for (var bi = 0; bi < bullets.length && bi < bulletPs.length; bi++) {
                                    if (bulletPs[bi].textContent.trim() !== bullets[bi]) {
                                        bulletPs[bi].textContent = bullets[bi];
                                    }
                                }
                            }
                        }
                    });

                    // Hide remaining boxes if fewer active services
                    for (var sIdx = DATA.services.length; sIdx < serviceBoxes.length; sIdx++) {
                        if (serviceBoxes[sIdx].style.display !== "none") {
                            serviceBoxes[sIdx].style.display = "none";
                        }
                    }
                }

                // 6. Stats & Metrics Sync (Years of Experience, Completed Projects, Clients on Worldwide, etc.)
                if (DATA.stat_experience_num) {
                    document.querySelectorAll('.framer-bev44h-container').forEach(function(box) {
                        box.querySelectorAll('h3').forEach(function(h) {
                            if (h.textContent.trim() !== DATA.stat_experience_num) h.textContent = DATA.stat_experience_num;
                        });
                        if (DATA.stat_experience_label) {
                            var p = box.querySelector('.framer-nnrta1 p');
                            if (p && p.textContent.trim() !== DATA.stat_experience_label) p.textContent = DATA.stat_experience_label;
                        }
                    });
                }

                if (DATA.stat_projects_num) {
                    document.querySelectorAll('.framer-wzht7u-container').forEach(function(box) {
                        box.querySelectorAll('h3').forEach(function(h) {
                            if (h.textContent.trim() !== DATA.stat_projects_num) h.textContent = DATA.stat_projects_num;
                        });
                        if (DATA.stat_projects_label) {
                            var p = box.querySelector('.framer-nnrta1 p');
                            if (p && p.textContent.trim() !== DATA.stat_projects_label) p.textContent = DATA.stat_projects_label;
                        }
                    });
                }

                if (DATA.stat_clients_num) {
                    document.querySelectorAll('.framer-wy4cwv-container').forEach(function(box) {
                        box.querySelectorAll('h3').forEach(function(h) {
                            if (h.textContent.trim() !== DATA.stat_clients_num) h.textContent = DATA.stat_clients_num;
                        });
                        if (DATA.stat_clients_label) {
                            var p = box.querySelector('.framer-nnrta1 p');
                            if (p && p.textContent.trim() !== DATA.stat_clients_label) p.textContent = DATA.stat_clients_label;
                        }
                    });
                }

                // General stat card fallback by matching label text
                document.querySelectorAll('.framer-bsCWJ').forEach(function(card) {
                    var labelEl = card.querySelector('.framer-nnrta1 p');
                    if (!labelEl) return;
                    var lTxt = labelEl.textContent.trim().toLowerCase();
                    var val = null;
                    if (lTxt.indexOf('experience') !== -1 && DATA.stat_experience_num) val = DATA.stat_experience_num;
                    else if (lTxt.indexOf('project') !== -1 && DATA.stat_projects_num) val = DATA.stat_projects_num;
                    else if (lTxt.indexOf('client') !== -1 && DATA.stat_clients_num) val = DATA.stat_clients_num;
                    else if (lTxt.indexOf('satisfaction') !== -1 && DATA.stat_satisfaction_num) val = DATA.stat_satisfaction_num;
                    else if (lTxt.indexOf('growth') !== -1 && DATA.stat_growth_num) val = DATA.stat_growth_num;

                    if (val) {
                        card.querySelectorAll('h3').forEach(function(h) {
                            if (h.textContent.trim() !== val) h.textContent = val;
                        });
                    }
                });

                // 7. Social Links Sync (X/Twitter, Instagram, Behance, Dribbble)
                if (DATA.twitter) {
                    document.querySelectorAll('a[href*="x.com"], a[href*="twitter.com"]').forEach(function(a) {
                        if (a.href !== DATA.twitter) a.href = DATA.twitter;
                    });
                }
                if (DATA.instagram) {
                    document.querySelectorAll('a[href*="instagram.com"]').forEach(function(a) {
                        if (a.href !== DATA.instagram) a.href = DATA.instagram;
                    });
                }
                if (DATA.behance) {
                    document.querySelectorAll('a[href*="behance.net"]').forEach(function(a) {
                        if (a.href !== DATA.behance) a.href = DATA.behance;
                    });
                }
                if (DATA.dribbble) {
                    document.querySelectorAll('a[href*="dribbble.com"]').forEach(function(a) {
                        if (a.href !== DATA.dribbble) a.href = DATA.dribbble;
                    });
                }

                // 8. Text Node Updates (Hero, About, Stats, Subtitles, Footer)
                var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                var node;
                while (node = walker.nextNode()) {
                    var text = node.nodeValue;
                    if (!text) continue;

                    // Phone across all occurrences (Hero, About, Contact)
                    if (DATA.phone && (text.indexOf("+1 (555)") !== -1 || text.indexOf("+1 (555) 777-8888") !== -1)) {
                        var newPhoneText = text.replace(/\\+1\\s*\\(555\\)\\s*123-4567/g, DATA.phone)
                                               .replace(/\\+1\\s*\\(555\\)\\s*777-8888/g, DATA.phone)
                                               .replace(/\\+1\\s*\\(555\\)/g, DATA.phone);
                        if (node.nodeValue !== newPhoneText) node.nodeValue = newPhoneText;
                    }

                    // Email across all occurrences
                    if (DATA.email && text.indexOf("designer@example.com") !== -1) {
                        var newEmailText = text.replace(/designer@example\\.com/g, DATA.email);
                        if (node.nodeValue !== newEmailText) node.nodeValue = newEmailText;
                    }

                    // Location & Availability
                    if (DATA.location && text.indexOf("Available for work") !== -1 && text.indexOf(DATA.location) === -1) {
                        var newLocText = "Available for work • " + DATA.location;
                        if (node.nodeValue !== newLocText) node.nodeValue = newLocText;
                    }

                    // Copyright
                    if (DATA.copyright && text.indexOf("Copyright 2025") !== -1 && node.nodeValue !== DATA.copyright) {
                        node.nodeValue = DATA.copyright;
                    }
                }
            } catch(e) {
                // Silently ignore
            } finally {
                isSyncing = false;
                if (obs && observerActive) {
                    try {
                        obs.observe(document.body, { childList: true, subtree: true, characterData: true });
                    } catch(e) {}
                }
            }
        }

        // Run immediately on page ready
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", syncContent);
        } else {
            syncContent();
        }

        window.addEventListener("load", syncContent);
        
        // Continuous debounced scroll listener ensures stats remain synchronized as user scrolls into view
        window.addEventListener("scroll", function() {
            if (debounceTimer) clearTimeout(debounceTimer);
            debounceTimer = setTimeout(syncContent, 30);
        }, { passive: true });

        // Run across staged intervals to catch initial React hydration & animation completion
        [100, 300, 600, 1000, 1500, 2200, 3200, 4500].forEach(function(delay) {
            setTimeout(syncContent, delay);
        });

        // Debounced MutationObserver to gracefully catch React component mount
        try {
            obs = new MutationObserver(function() {
                if (isSyncing || !observerActive) return;
                if (debounceTimer) clearTimeout(debounceTimer);
                debounceTimer = setTimeout(syncContent, 50);
            });
            obs.observe(document.body, { childList: true, subtree: true, characterData: true });
        } catch(e) {}
    })();
    </script>
    </body>
    '''
    # 3. Replace Global Designer Info on raw HTML FIRST (before script injection!)
    if site_settings.designer_name:
        html = html.replace("Duncan Robert", site_settings.designer_name)
    if site_settings.email:
        html = html.replace("designer@example.com", site_settings.email)
    if site_settings.phone:
        html = html.replace("+1 (555) 123-4567", site_settings.phone)
        html = html.replace("+1 (555) 777-8888", site_settings.phone)
        html = html.replace("+1 (555)", site_settings.phone)
    if site_settings.twitter_url:
        html = re.sub(r'href="https?://(?:www\.)?(?:x\.com|twitter\.com)[^"]*"', f'href="{site_settings.twitter_url}"', html)
    if site_settings.instagram_url:
        html = re.sub(r'href="https?://(?:www\.)?instagram\.com[^"]*"', f'href="{site_settings.instagram_url}"', html)
    if site_settings.behance_url:
        html = re.sub(r'href="https?://(?:www\.)?behance\.net[^"]*"', f'href="{site_settings.behance_url}"', html)
    if site_settings.dribbble_url:
        html = re.sub(r'href="https?://(?:www\.)?dribbble\.com[^"]*"', f'href="{site_settings.dribbble_url}"', html)
    avatar_url = payload.get("avatar_url")
    services_img = payload.get("services_image_url") or avatar_url

    if avatar_url:
        # Front face of 3D card (qrx)
        html = re.sub(r'https?://[^\s"\']+/images/qrxY8NagVO40NBrdhFEGgFR3PYY[^\s"\']*', avatar_url, html)
        html = re.sub(r'(?:/|\.\./)?framerusercontent\.com/images/qrxY8NagVO40NBrdhFEGgFR3PYY[^\s"\']*', avatar_url, html)
        # Floating Navbar circular avatar (IUYre)
        html = re.sub(r'https?://[^\s"\']+/images/IUYreEo8ON7qCLgK2tgDOW0xoI[^\s"\']*', avatar_url, html)
        html = re.sub(r'(?:/|\.\./)?framerusercontent\.com/images/IUYreEo8ON7qCLgK2tgDOW0xoI[^\s"\']*', avatar_url, html)

    if services_img:
        # Back face of 3D card / Services card (VRQ)
        html = re.sub(r'https?://[^\s"\']+/images/VRQgkdWsjawSg1qpCm45HfSY1I[^\s"\']*', services_img, html)
        html = re.sub(r'(?:/|\.\./)?framerusercontent\.com/images/VRQgkdWsjawSg1qpCm45HfSY1I[^\s"\']*', services_img, html)

    # Services Subtitle SSR replacement
    if site_settings.services_subtitle:
        html = html.replace(
            "As a digital designer, I am a visual storyteller, crafting experiences that connect deeply and spark creativity.",
            site_settings.services_subtitle
        )

    # Services Titles SSR replacement
    default_service_titles = [
        "1. ui/ux design",
        "2. Graphic Design",
        "3. Web Design",
        "4. Branding",
    ]
    for idx, def_title in enumerate(default_service_titles):
        if idx < len(active_services):
            srv = active_services[idx]
            new_title = f"{srv.order_num} {srv.title}".strip()
            html = html.replace(def_title, new_title)

    # Strip Framer promo widgets and badge containers from SSR raw HTML
    html = re.sub(r'<div class="framer-rcd755-container[^"]*"[^>]*>.*?</a><!--/\$--></div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div class="framer-1fin31n-container[^"]*"[^>]*>.*?</div></div>', '', html, flags=re.DOTALL)
    html = re.sub(r'<div id="__framer-badge-container"[^>]*>.*?</div>\s*</div>', '', html, flags=re.DOTALL)

    # 4. Now inject the clean synchronizer script (untouched by replacements)
    sync_script = sync_script_template.replace("__PAYLOAD_JSON__", payload_json)
    html = html.replace('</body>', sync_script)

    # 4. If on project detail page, dynamically update project content
    if context_type == "project" and item_slug:
        try:
            proj = Project.objects.get(slug=item_slug)
            if proj.tagline:
                # Replace original tagline if found
                pass
            if proj.client:
                html = html.replace("Studio Prism", proj.client)
            if proj.year:
                html = html.replace("2025", str(proj.year))
            if proj.industry:
                html = html.replace("Tech", proj.industry)
            if proj.duration:
                html = html.replace("4 weeks", proj.duration)
            if proj.cover_url:
                # Replace main cover image
                orig_img = proj.cover_image_static
                if orig_img and proj.cover_image:
                    html = html.replace(orig_img, proj.cover_image.url.lstrip('/'))
        except Project.DoesNotExist:
            pass

    # 5. Fix link targets so they route cleanly through Django
    html = re.sub(r'href="about\.html"', 'href="/about/"', html)
    html = re.sub(r'href="projects\.html"', 'href="/projects/"', html)
    html = re.sub(r'href="blogs\.html"', 'href="/blogs/"', html)
    html = re.sub(r'href="index\.html"', 'href="/"', html)
    html = re.sub(r'href="projects/([^"]+)\.html"', r'href="/projects/\1/"', html)
    html = re.sub(r'href="blogs/([^"]+)\.html"', r'href="/blogs/\1/"', html)

    return html


def framer_home_view(request):
    file_path = os.path.join(FRAMER_DIR, "index.html")
    if not os.path.exists(file_path):
        raise Http404("Framer index.html not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="home")
    return HttpResponse(rendered_html, content_type="text/html")


def framer_about_view(request):
    file_path = os.path.join(FRAMER_DIR, "about.html")
    if not os.path.exists(file_path):
        raise Http404("Framer about.html not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="about")
    return HttpResponse(rendered_html, content_type="text/html")


def framer_projects_view(request):
    file_path = os.path.join(FRAMER_DIR, "projects.html")
    if not os.path.exists(file_path):
        raise Http404("Framer projects.html not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="projects")
    return HttpResponse(rendered_html, content_type="text/html")


def framer_project_detail_view(request, slug):
    # Try exact html file first
    file_path = os.path.join(FRAMER_DIR, "projects", f"{slug}.html")
    if not os.path.exists(file_path):
        # Fallback to any project template or 404
        fallback_files = [f for f in os.listdir(os.path.join(FRAMER_DIR, "projects")) if f.endswith(".html")]
        if fallback_files:
            file_path = os.path.join(FRAMER_DIR, "projects", fallback_files[0])
        else:
            raise Http404("Project case study not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="project", item_slug=slug)
    return HttpResponse(rendered_html, content_type="text/html")


def framer_blogs_view(request):
    file_path = os.path.join(FRAMER_DIR, "blogs.html")
    if not os.path.exists(file_path):
        raise Http404("Framer blogs.html not found.")
    
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="blogs")
    return HttpResponse(rendered_html, content_type="text/html")


def framer_blog_detail_view(request, slug):
    file_path = os.path.join(FRAMER_DIR, "blogs", f"{slug}.html")
    if not os.path.exists(file_path):
        fallback_files = [f for f in os.listdir(os.path.join(FRAMER_DIR, "blogs")) if f.endswith(".html")]
        if fallback_files:
            file_path = os.path.join(FRAMER_DIR, "blogs", fallback_files[0])
        else:
            raise Http404("Blog post not found.")

    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    rendered_html = _inject_dynamic_data(html, context_type="blog", item_slug=slug)
    return HttpResponse(rendered_html, content_type="text/html")
