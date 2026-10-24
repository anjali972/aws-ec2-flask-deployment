from flask import Flask, render_template_string, jsonify
import socket
from datetime import datetime, timezone

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <meta name="theme-color" content="#080d1a">
    <meta name="description"
          content="Cloud engineering portfolio featuring AWS,
          infrastructure security, networking and application deployment.">

    <title>Cloud Engineering | Portfolio</title>

    <style>
        :root {
            --bg: #080d1a;
            --surface: #101829;
            --surface-light: #151f33;
            --border: rgba(148, 163, 184, 0.16);
            --text: #f1f5f9;
            --muted: #9ba9bf;
            --blue: #60a5fa;
            --cyan: #67e8f9;
            --green: #4ade80;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
            scroll-padding-top: 90px;
        }

        body {
            font-family: Inter, -apple-system, BlinkMacSystemFont,
                         "Segoe UI", sans-serif;
            background:
                radial-gradient(
                    ellipse at 80% 0%,
                    rgba(37, 99, 235, 0.13),
                    transparent 35%
                ),
                var(--bg);
            color: var(--text);
            line-height: 1.7;
            overflow-x: hidden;
        }

        a {
            color: inherit;
            text-decoration: none;
        }

        .container {
            width: min(1100px, 90%);
            margin: 0 auto;
        }

        /* Navigation */

        header {
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(8, 13, 26, 0.88);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid var(--border);
        }

        nav {
            min-height: 76px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        .logo {
            font-size: 1.12rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .logo span {
            color: var(--blue);
        }

        .nav-links {
            display: flex;
            align-items: center;
            gap: 30px;
            list-style: none;
            font-size: 0.91rem;
            color: var(--muted);
        }

        .nav-links a:hover {
            color: var(--cyan);
        }

        .nav-cta {
            color: var(--text) !important;
            padding: 9px 16px;
            border: 1px solid var(--border);
            border-radius: 9px;
        }

        /* Hero */

        .hero {
            min-height: 590px;
            display: grid;
            grid-template-columns: 1.25fr 0.75fr;
            align-items: center;
            gap: 55px;
            padding-top: 75px;
            padding-bottom: 85px;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            color: var(--cyan);
            text-transform: uppercase;
            letter-spacing: 2.2px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 25px;
        }

        .eyebrow::before {
            content: "";
            width: 25px;
            height: 2px;
            background: var(--cyan);
        }

        h1 {
            max-width: 700px;
            font-size: clamp(2.7rem, 5.6vw, 4.8rem);
            line-height: 1.08;
            letter-spacing: -3px;
            margin-bottom: 25px;
        }

        .gradient-text {
            background: linear-gradient(
                100deg,
                #60a5fa,
                #67e8f9
            );
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }

        .hero-description {
            max-width: 570px;
            font-size: 1.04rem;
            color: var(--muted);
            line-height: 1.9;
            margin-bottom: 30px;
        }

        .buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            margin-bottom: 32px;
        }

        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 20px;
            border-radius: 9px;
            font-size: 0.92rem;
            font-weight: 700;
            transition: transform 0.2s, background 0.2s;
        }

        .button:hover {
            transform: translateY(-2px);
        }

        .button-primary {
            background: var(--blue);
            color: #08111f;
        }

        .button-primary:hover {
            background: var(--cyan);
        }

        .button-secondary {
            border: 1px solid var(--border);
            color: var(--text);
        }

        .button-secondary:hover {
            background: var(--surface-light);
        }

        .hero-note {
            color: var(--muted);
            font-size: 0.82rem;
        }

        .hero-note strong {
            color: var(--green);
            font-weight: 600;
        }

        /* Terminal card */

        .terminal {
            background: rgba(16, 24, 41, 0.92);
            border: 1px solid rgba(96, 165, 250, 0.25);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 25px 90px rgba(0, 0, 0, 0.3);
            transform: rotate(1deg);
        }

        .terminal-bar {
            height: 47px;
            padding: 0 17px;
            display: flex;
            align-items: center;
            gap: 7px;
            background: rgba(255, 255, 255, 0.025);
            border-bottom: 1px solid var(--border);
        }

        .dot {
            height: 9px;
            width: 9px;
            border-radius: 50%;
            background: #64748b;
        }

        .terminal-title {
            margin-left: auto;
            color: var(--muted);
            font-size: 0.72rem;
        }

        .terminal-body {
            padding: 25px 23px 29px;
            font-family: "SFMono-Regular", Consolas, monospace;
            font-size: 0.84rem;
            overflow-wrap: anywhere;
        }

        .terminal-line {
            margin-bottom: 17px;
            color: var(--muted);
        }

        .terminal-prompt {
            color: var(--green);
        }

        .terminal-blue {
            color: var(--blue);
        }

        .terminal-value {
            color: var(--cyan);
        }

        .terminal-divider {
            height: 1px;
            background: var(--border);
            margin: 21px 0;
        }

        .terminal-status {
            display: flex;
            align-items: center;
            gap: 9px;
            color: var(--green);
            font-family: Inter, sans-serif;
            font-size: 0.86rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            flex-shrink: 0;
            border-radius: 50%;
            background: var(--green);
            box-shadow: 0 0 12px rgba(74, 222, 128, 0.55);
        }

        /* Technology strip */

        .tech-strip {
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            background: rgba(16, 24, 41, 0.52);
        }

        .tech-inner {
            min-height: 112px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 20px;
            padding-top: 25px;
            padding-bottom: 25px;
        }

        .tech-label {
            width: 100%;
            color: var(--muted);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .tech-item {
            color: #d2dbea;
            font-weight: 700;
            font-size: 0.95rem;
        }

        /* General sections */

        section {
            padding: 100px 0;
        }

        .section-heading {
            margin-bottom: 45px;
        }

        .section-kicker {
            color: var(--blue);
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.73rem;
            font-weight: 700;
            margin-bottom: 12px;
        }

        h2 {
            font-size: clamp(2rem, 4vw, 2.7rem);
            letter-spacing: -1.2px;
            line-height: 1.2;
            margin-bottom: 14px;
        }

        .section-description {
            max-width: 660px;
            color: var(--muted);
        }

        /* Project cards */

        .projects-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 22px;
        }

        .project-card {
            padding: 29px;
            background: linear-gradient(
                145deg,
                rgba(21, 31, 51, 0.92),
                rgba(16, 24, 41, 0.92)
            );
            border: 1px solid var(--border);
            border-radius: 14px;
            transition: border-color 0.25s, transform 0.25s;
        }

        .project-card:hover {
            transform: translateY(-5px);
            border-color: rgba(96, 165, 250, 0.65);
        }

        .project-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-bottom: 23px;
        }

        .project-number {
            color: var(--blue);
            font-family: monospace;
            font-size: 0.95rem;
        }

        .project-label {
            color: var(--muted);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 4px 10px;
            font-size: 0.7rem;
        }

        h3 {
            font-size: 1.18rem;
            margin-bottom: 13px;
            line-height: 1.4;
        }

        .project-description {
            color: var(--muted);
            font-size: 0.91rem;
            line-height: 1.85;
            margin-bottom: 22px;
        }

        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .tag {
            padding: 5px 10px;
            color: #b9d7ff;
            background: rgba(96, 165, 250, 0.09);
            border: 1px solid rgba(96, 165, 250, 0.14);
            border-radius: 6px;
            font-size: 0.73rem;
        }

        /* Architecture */

        .architecture {
            background: rgba(16, 24, 41, 0.55);
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
        }

        .architecture-flow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
            margin-top: 35px;
        }

        .architecture-step {
            position: relative;
            padding: 22px 14px;
            text-align: center;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .architecture-step:not(:last-child)::after {
            content: "→";
            position: absolute;
            right: -14px;
            top: 50%;
            z-index: 2;
            transform: translateY(-50%);
            color: var(--cyan);
            font-size: 1.2rem;
        }

        .architecture-step strong {
            display: block;
            font-size: 0.92rem;
            margin-bottom: 7px;
        }

        .architecture-step span {
            color: var(--muted);
            font-size: 0.78rem;
        }

        .architecture-note {
            color: var(--muted);
            margin-top: 22px;
            font-size: 0.86rem;
        }

        /* About */

        .about-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 45px;
            align-items: start;
        }

        .about-copy {
            color: var(--muted);
            line-height: 1.95;
        }

        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .skill {
            padding: 10px 14px;
            border-radius: 8px;
            background: var(--surface);
            border: 1px solid var(--border);
            color: #dbeafe;
            font-size: 0.85rem;
        }

        /* Footer */

        footer {
            padding: 28px 0;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.82rem;
        }

        .footer-inner {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .footer-status {
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        /* Responsive design */

        @media (max-width: 800px) {
            .hero {
                grid-template-columns: 1fr;
                gap: 40px;
                min-height: auto;
                padding-top: 75px;
                padding-bottom: 65px;
            }

            .terminal {
                max-width: 520px;
                width: 100%;
                transform: none;
            }

            .projects-grid {
                grid-template-columns: 1fr;
            }

            .architecture-flow {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 14px;
            }

            .architecture-step::after {
                display: none;
            }

            .about-grid {
                grid-template-columns: 1fr;
                gap: 30px;
            }

            .tech-inner {
                justify-content: flex-start;
            }

            .tech-item {
                min-width: 25%;
            }
        }

        @media (max-width: 520px) {
            .container {
                width: 88%;
            }

            nav {
                min-height: 68px;
            }

            .nav-links {
                gap: 13px;
                font-size: 0.78rem;
            }

            .nav-links .nav-cta {
                display: none;
            }

            h1 {
                letter-spacing: -1.8px;
                font-size: 2.65rem;
            }

            section {
                padding: 70px 0;
            }

            .project-card {
                padding: 22px;
            }

            .architecture-flow {
                grid-template-columns: 1fr 1fr;
            }

            .terminal-body {
                padding: 21px 16px;
                font-size: 0.76rem;
            }

            .footer-inner {
                align-items: flex-start;
                flex-direction: column;
            }
        }

        @media (prefers-reduced-motion: reduce) {
            html {
                scroll-behavior: auto;
            }

            *, *::before, *::after {
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>

<body>

<header>
    <nav class="container">
        <a href="#home" class="logo">cloud<span>.portfolio</span></a>

        <ul class="nav-links">
            <li><a href="#projects">Projects</a></li>
            <li><a href="#architecture">Architecture</a></li>
            <li><a href="#about">Skills</a></li>
            <li><a href="#about" class="nav-cta">About Me ↗</a></li>
        </ul>
    </nav>
</header>

<main>

    <!-- Hero section -->
    <section class="container hero" id="home">

        <div>
            <div class="eyebrow">Cloud &amp; DevOps Engineering</div>

            <h1>
                Building in the cloud.
                <span class="gradient-text">Automating with purpose.</span>
            </h1>

            <p class="hero-description">
                I explore cloud infrastructure, security, networking,
                and application deployment through hands-on engineering
                projects. My focus is on understanding not just how
                systems work, but why they are designed that way.
            </p>

            <div class="buttons">
                <a class="button button-primary" href="#projects">
                    Explore Projects ↘
                </a>

                <a class="button button-secondary" href="#about">
                    Explore My Skills
                </a>
            </div>

            <p class="hero-note">
                <strong>●</strong>
                Learning by building, testing, and documenting.
            </p>
        </div>

        <div class="terminal">
            <div class="terminal-bar">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="terminal-title">cloud-environment</span>
            </div>

            <div class="terminal-body">

                <p class="terminal-line">
                    <span class="terminal-prompt">$</span>
                    whoami
                </p>

                <p class="terminal-blue">cloud_engineer_in_training</p>

                <div class="terminal-divider"></div>

                <p class="terminal-line">
                    <span class="terminal-prompt">$</span>
                    systemctl status mysite
                </p>

                <p class="terminal-value">● Application service</p>
                <p style="margin-top: 7px;">Loaded: systemd service</p>
                <p>Server: Gunicorn + Flask</p>
                <p>Proxy: Nginx</p>

                <div class="terminal-divider"></div>

                <div class="terminal-status">
                    <span class="status-dot"></span>
                    EC2 application endpoint responding
                </div>

                <p style="margin-top: 17px; color: var(--muted);">
                    Host: {{ host }}
                </p>

                <p style="margin-top: 7px; color: var(--muted);">
                    UTC: {{ time }}
                </p>

            </div>
        </div>

    </section>

    <!-- Technology strip -->
    <div class="tech-strip">
        <div class="container tech-inner">

            <p class="tech-label">Technologies in my projects</p>

            <span class="tech-item">AWS</span>
            <span class="tech-item">Linux</span>
            <span class="tech-item">Python</span>
            <span class="tech-item">Terraform</span>
            <span class="tech-item">Nginx</span>
            <span class="tech-item">Git</span>

        </div>
    </div>

    <!-- Projects -->
    <section class="container" id="projects">

        <div class="section-heading">
            <p class="section-kicker">Selected Work</p>

            <h2>Engineering through projects.</h2>

            <p class="section-description">
                Practical cloud projects focused on access control,
                infrastructure, networking, and deployment.
            </p>
        </div>

        <div class="projects-grid">

            <article class="project-card">

                <div class="project-top">
                    <span class="project-number">01 / SECURITY</span>
                    <span class="project-label">AWS IAM</span>
                </div>

                <h3>Least-Privilege Access Control</h3>

                <p class="project-description">
                    Configured identity-based access controls and tested
                    allowed and denied S3 operations to understand how
                    least-privilege permissions restrict access to
                    cloud resources.
                </p>

                <div class="tags">
                    <span class="tag">IAM</span>
                    <span class="tag">S3</span>
                    <span class="tag">Policies</span>
                    <span class="tag">Access Testing</span>
                </div>

            </article>

            <article class="project-card">

                <div class="project-top">
                    <span class="project-number">02 / NETWORKING</span>
                    <span class="project-label">AWS VPC</span>
                </div>

                <h3>Cloud Network Design &amp; Validation</h3>

                <p class="project-description">
                    Explored segmented cloud networking, subnet design,
                    traffic flow, and security controls while validating
                    connectivity between network components.
                </p>

                <div class="tags">
                    <span class="tag">VPC</span>
                    <span class="tag">Subnets</span>
                    <span class="tag">Routing</span>
                    <span class="tag">Security Groups</span>
                </div>

            </article>

            <article class="project-card">

                <div class="project-top">
                    <span class="project-number">03 / STORAGE</span>
                    <span class="project-label">Amazon S3</span>
                </div>

                <h3>Static Website &amp; Object Versioning</h3>

                <p class="project-description">
                    Configured static website hosting, bucket access
                    policies, and object versioning. Tested access
                    restrictions and examined how previous object
                    versions can support recovery.
                </p>

                <div class="tags">
                    <span class="tag">S3</span>
                    <span class="tag">Bucket Policies</span>
                    <span class="tag">Versioning</span>
                    <span class="tag">Static Hosting</span>
                </div>

            </article>

            <article class="project-card">

                <div class="project-top">
                    <span class="project-number">04 / DEPLOYMENT</span>
                    <span class="project-label">AWS EC2</span>
                </div>

                <h3>Flask Deployment with Nginx</h3>

                <p class="project-description">
                    Deployed a Python web application on EC2, configured
                    Gunicorn as the WSGI application server, managed it
                    with systemd, and used Nginx as a reverse proxy.
                </p>

                <div class="tags">
                    <span class="tag">EC2</span>
                    <span class="tag">Flask</span>
                    <span class="tag">Gunicorn</span>
                    <span class="tag">Nginx</span>
                    <span class="tag">systemd</span>
                </div>

            </article>

        </div>

    </section>

    <!-- Deployment architecture -->
    <section class="architecture" id="architecture">

        <div class="container">

            <div class="section-heading">
                <p class="section-kicker">Under the Hood</p>

                <h2>How this website runs.</h2>

                <p class="section-description">
                    A look at the request path through the application
                    stack deployed on the EC2 instance.
                </p>
            </div>

            <div class="architecture-flow">

                <div class="architecture-step">
                    <strong>Browser</strong>
                    <span>HTTP request</span>
                </div>

                <div class="architecture-step">
                    <strong>Nginx</strong>
                    <span>Reverse proxy · Port 80</span>
                </div>

                <div class="architecture-step">
                    <strong>Gunicorn</strong>
                    <span>WSGI server · Local port 8000</span>
                </div>

                <div class="architecture-step">
                    <strong>Flask</strong>
                    <span>Python application</span>
                </div>

            </div>

            <p class="architecture-note">
                Gunicorn listens on the local interface, while Nginx
                accepts public HTTP requests. The EC2 security group
                does not need to expose port 8000.
            </p>

        </div>

    </section>

    <!-- About and skills -->
    <section class="container" id="about">

        <div class="about-grid">

            <div>
                <p class="section-kicker">About This Portfolio</p>

                <h2>Learning by building real systems.</h2>

                <p class="about-copy">
                    This portfolio documents my journey into cloud
                    engineering and DevOps. Through practical projects,
                    I am learning to configure infrastructure, apply
                    security controls, troubleshoot deployments, and
                    understand how application components work together.
                    <br><br>
                    My goal is to build reliable systems, document
                    technical decisions clearly, and keep improving
                    through hands-on experimentation.
                </p>
            </div>

            <div>
                <p class="section-kicker">Technical Toolkit</p>

                <h2>Tools &amp; technologies.</h2>

                <div class="skills-grid">
                    <span class="skill">AWS EC2</span>
                    <span class="skill">AWS IAM</span>
                    <span class="skill">Amazon S3</span>
                    <span class="skill">Amazon VPC</span>
                    <span class="skill">Linux</span>
                    <span class="skill">Python</span>
                    <span class="skill">Flask</span>
                    <span class="skill">Gunicorn</span>
                    <span class="skill">Nginx</span>
                    <span class="skill">systemd</span>
                    <span class="skill">Terraform</span>
                    <span class="skill">Git</span>
                </div>
            </div>

        </div>

    </section>

</main>

<footer>
    <div class="container footer-inner">

        <p>
            Built with Flask · Deployed on AWS EC2
        </p>

        <p class="footer-status">
            <span class="status-dot"></span>
            Server responded · {{ time }}
        </p>

    </div>
</footer>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE,
        host=socket.gethostname(),
        time=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    )


@app.route("/health")
def health():
    return jsonify(
        status="ok",
        application="mysite",
        timestamp=datetime.now(timezone.utc).isoformat()
    ), 200


if __name__ == "__main__":
    app.run()
