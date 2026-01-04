DROP TABLE IF EXISTS translations CASCADE;
DROP TABLE IF EXISTS content_items CASCADE;
DROP TABLE IF EXISTS pages CASCADE;
DROP TABLE IF EXISTS settings CASCADE;
DROP TABLE IF EXISTS users CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT,
    modified_at TIMESTAMP
);

CREATE TABLE settings (
    id BIGSERIAL PRIMARY KEY,
    reference_key VARCHAR(255) NOT NULL,
    value TEXT NOT NULL,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);
-- Create Pages table
CREATE TABLE pages (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

CREATE TABLE content_items (
    id BIGSERIAL PRIMARY KEY,
    page_id BIGINT REFERENCES pages(id),
    position INT NOT NULL,
    title VARCHAR(255),
    content TEXT,
    content_type VARCHAR(50) NOT NULL,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

CREATE TABLE translations (
    id BIGSERIAL PRIMARY KEY,
    reference_key VARCHAR(255) NOT NULL,
    language VARCHAR(10) NOT NULL,
    text TEXT,
    added_by BIGINT REFERENCES users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    modified_by BIGINT REFERENCES users(id),
    modified_at TIMESTAMP
);

INSERT INTO users (username, password_hash, role) VALUES
('admin', '$2b$12$r2kXcGXkML843/gNLnCbVumbXV5lNalec/4Ly1p9TERdIzwUCzLhy', 'admin'),
('editor', '$2b$12$SqMhJCQ5LVoUF.cXCYXB5O9bzUEeB/ORbCcFJoFtmVdQzuvT36.K.', 'editor'),
('viewer', '$2b$12$La5OlsMGX9YlR7k9Ow.XL.Tvd2uNE5CM2vok.2TlpT0ttlGeVok5K', 'viewer');

INSERT INTO settings (reference_key, value, added_by) VALUES
('site_title', 'CarServ - Car Repair Service Center', 1),
('site_logo', '<i class="fa fa-car me-3"></i>CarServ', 1),
('contact_address', '123 Street, New York, USA', 1),
('contact_phone', '+012 345 6789', 1),
('contact_email', 'info@carserv.com', 1),
('opening_hours_weekday', 'Mon - Fri : 09.00 AM - 09.00 PM', 1),
('opening_hours_weekend', 'Sat - Sun : 09.00 AM - 12.00 PM', 1),
('facebook_url', 'https://facebook.com', 1),
('twitter_url', 'https://twitter.com', 1),
('linkedin_url', 'https://linkedin.com', 1),
('instagram_url', 'https://instagram.com', 1),
('years_experience', '15', 1),
('stats_experience', '1234', 1),
('stats_technicians', '1234', 1),
('stats_clients', '1234', 1),
('stats_projects', '1234', 1);
-- Seed Pages
INSERT INTO pages (name, slug, added_by) VALUES
('Home', 'home', 1),
('About', 'about', 1),
('Services', 'services', 1),
('Contact', 'contact', 1),
('Team', 'team', 1),
('Testimonials', 'testimonials', 1),
('Booking', 'booking', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(1, 1, 'Qualified Car Repair Service Center', '// Car Servicing //', 'carousel', 1),
(1, 2, 'Qualified Car Wash Service Center', '// Car Servicing //', 'carousel', 1),
(1, 3, 'Quality Servicing', 'Diam dolor diam ipsum sit amet diam et eos erat ipsum', 'feature', 1),
(1, 4, 'Expert Workers', 'Diam dolor diam ipsum sit amet diam et eos erat ipsum', 'feature', 1),
(1, 5, 'Modern Equipment', 'Diam dolor diam ipsum sit amet diam et eos erat ipsum', 'feature', 1),
(1, 6, 'CarServ Is The Best Place For Your Auto Care', 'Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet', 'about', 1),
(1, 7, 'Professional & Expert', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1),
(1, 8, 'Quality Servicing Center', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1),
(1, 9, 'Awards Winning Workers', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1),
(1, 10, 'Certified and Award Winning Car Repair Service Provider', 'Eirmod sed tempor lorem ut dolores. Aliquyam sit sadipscing kasd ipsum. Dolor ea et dolore et at sea ea at dolor, justo ipsum duo rebum sea invidunt voluptua. Eos vero eos vero ea et dolore eirmod et. Dolores diam duo invidunt lorem. Elitr ut dolores magna sit. Sea dolore sanctus sed et. Takimata takimata sanctus sed.', 'booking_info', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(2, 1, '// About Us //', 'About Us', 'page_header', 1),
(2, 2, 'CarServ Is The Best Place For Your Auto Care', 'Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet', 'about', 1),
(2, 3, 'Professional & Expert', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1),
(2, 4, 'Quality Servicing Center', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1),
(2, 5, 'Awards Winning Workers', 'Diam dolor diam ipsum sit amet diam et eos', 'about_point', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(3, 1, '// Our Services //', 'Explore Our Services', 'page_header', 1),
(3, 2, 'Diagnostic Test', '15 Years Of Experience In Auto Servicing||Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet||Quality Servicing||Expert Workers||Modern Equipment||img/service-1.jpg', 'service', 1),
(3, 3, 'Engine Servicing', '15 Years Of Experience In Auto Servicing||Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet||Quality Servicing||Expert Workers||Modern Equipment||img/service-2.jpg', 'service', 1),
(3, 4, 'Tires Replacement', '15 Years Of Experience In Auto Servicing||Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet||Quality Servicing||Expert Workers||Modern Equipment||img/service-3.jpg', 'service', 1),
(3, 5, 'Oil Changing', '15 Years Of Experience In Auto Servicing||Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit. Aliqu diam amet diam et eos. Clita erat ipsum et lorem et sit, sed stet lorem sit clita duo justo magna dolore erat amet||Quality Servicing||Expert Workers||Modern Equipment||img/service-4.jpg', 'service', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(4, 1, '// Contact Us //', 'Contact For Any Query', 'page_header', 1),
(4, 2, 'Get In Touch', 'Contact us for any questions or inquiries about our services', 'contact_intro', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(5, 1, '// Our Technicians //', 'Our Expert Technicians', 'page_header', 1),
(5, 2, 'John Smith', 'Master Technician||img/team-1.jpg||https://facebook.com||https://twitter.com||https://instagram.com', 'team_member', 1),
(5, 3, 'Sarah Johnson', 'Engine Specialist||img/team-2.jpg||https://facebook.com||https://twitter.com||https://instagram.com', 'team_member', 1),
(5, 4, 'Mike Wilson', 'Senior Mechanic||img/team-3.jpg||https://facebook.com||https://twitter.com||https://instagram.com', 'team_member', 1),
(5, 5, 'David Brown', 'Diagnostic Expert||img/team-4.jpg||https://facebook.com||https://twitter.com||https://instagram.com', 'team_member', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(6, 1, '// Testimonial //', 'Our Clients Say!', 'page_header', 1),
(6, 2, 'Robert Johnson', 'Business Owner||Tempor erat elitr rebum at clita. Diam dolor diam ipsum sit diam amet diam et eos. Clita erat ipsum et lorem et sit.||img/testimonial-1.jpg', 'testimonial', 1),
(6, 3, 'Maria Garcia', 'Software Engineer||Excellent service! My car runs like new after their maintenance work. Highly professional team.||img/testimonial-2.jpg', 'testimonial', 1),
(6, 4, 'James Wilson', 'Teacher||Best car service in town. They are honest, efficient, and their prices are very reasonable.||img/testimonial-3.jpg', 'testimonial', 1),
(6, 5, 'Lisa Anderson', 'Entrepreneur||I trust them with all my vehicles. Great customer service and quality work every time.||img/testimonial-4.jpg', 'testimonial', 1);

INSERT INTO content_items (page_id, position, title, content, content_type, added_by) VALUES
(7, 1, '// Booking //', 'Book A Service', 'page_header', 1),
(7, 2, 'Book For A Service', 'Fill out the form below to schedule your service appointment', 'booking_form', 1);

INSERT INTO translations (reference_key, language, text, added_by) VALUES
('nav_home', 'en', 'Home', 1),
('nav_about', 'en', 'About', 1),
('nav_services', 'en', 'Services', 1),
('nav_contact', 'en', 'Contact', 1),
('btn_get_quote', 'en', 'Get A Quote', 1),
('btn_learn_more', 'en', 'Learn More', 1),
('btn_read_more', 'en', 'Read More', 1),
('btn_book_now', 'en', 'Book Now', 1);

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'admin') THEN

      CREATE ROLE admin LOGIN PASSWORD 'admin';
      ALTER ROLE admin WITH SUPERUSER;
   END IF;
END
$do$;
