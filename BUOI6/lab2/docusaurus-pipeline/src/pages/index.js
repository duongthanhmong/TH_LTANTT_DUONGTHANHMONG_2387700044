import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout title="BUOI6 DevSecOps" description="Bài thực hành DevSecOps">
      <main>
        <header className="hero hero--primary">
          <div className="container">
            <h1 className="hero__title">BUOI6 - DevSecOps</h1>
            <p className="hero__subtitle">Build artifact và triển khai GitLab Pages</p>
            <Link className="button button--secondary button--lg" to="/docs/intro">
              Xem tài liệu pipeline
            </Link>
          </div>
        </header>
      </main>
    </Layout>
  );
}
