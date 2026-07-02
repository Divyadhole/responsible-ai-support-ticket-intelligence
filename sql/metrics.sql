CREATE INDEX idx_ticket_segment ON tickets(language, channel);
CREATE INDEX idx_ticket_outcomes ON tickets(automated, correct, true_queue, predicted_queue);

CREATE VIEW model_summary AS
SELECT COUNT(*) tickets,
 ROUND(100.0*SUM(correct)/COUNT(*),2) accuracy_pct,
 ROUND(100.0*SUM(automated)/COUNT(*),2) automation_pct,
 ROUND(100.0*SUM(CASE WHEN automated=1 THEN correct ELSE 0 END)/NULLIF(SUM(automated),0),2) automated_accuracy_pct,
 ROUND(AVG(confidence),3) avg_confidence,
 ROUND(AVG(latency_ms),1) avg_latency_ms,
 ROUND(SUM(estimated_cost_usd),2) total_cost_usd
FROM tickets;

CREATE VIEW subgroup_metrics AS
SELECT language, channel, COUNT(*) tickets,
 ROUND(100.0*SUM(correct)/COUNT(*),2) accuracy_pct,
 ROUND(100.0*SUM(automated)/COUNT(*),2) automation_pct,
 ROUND(AVG(confidence),3) avg_confidence
FROM tickets GROUP BY language, channel ORDER BY language, channel;

CREATE VIEW language_metrics AS
SELECT language, COUNT(*) tickets,
 ROUND(100.0*SUM(correct)/COUNT(*),2) accuracy_pct,
 ROUND(100.0*SUM(automated)/COUNT(*),2) automation_pct,
 ROUND(100.0*SUM(CASE WHEN automated=1 THEN correct ELSE 0 END)/NULLIF(SUM(automated),0),2) automated_accuracy_pct,
 ROUND(AVG(confidence),3) avg_confidence
FROM tickets GROUP BY language ORDER BY tickets DESC;

CREATE VIEW queue_metrics AS
SELECT true_queue, COUNT(*) tickets,
 ROUND(100.0*SUM(correct)/COUNT(*),2) recall_pct,
 ROUND(100.0*SUM(automated)/COUNT(*),2) automation_pct
FROM tickets GROUP BY true_queue ORDER BY tickets DESC;

CREATE VIEW confusion_matrix AS
SELECT true_queue, predicted_queue, COUNT(*) tickets
FROM tickets GROUP BY true_queue, predicted_queue ORDER BY true_queue, predicted_queue;

CREATE VIEW review_queue AS
SELECT review_reason, COUNT(*) tickets,
 ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM tickets WHERE automated=0),2) review_share_pct,
 ROUND(100.0*SUM(correct)/COUNT(*),2) pre_review_accuracy_pct
FROM tickets WHERE automated=0 GROUP BY review_reason ORDER BY tickets DESC;

CREATE VIEW daily_monitoring AS
SELECT DATE(created_at) date, COUNT(*) tickets,
 ROUND(100.0*SUM(correct)/COUNT(*),2) accuracy_pct,
 ROUND(100.0*SUM(automated)/COUNT(*),2) automation_pct,
 ROUND(AVG(latency_ms),1) avg_latency_ms
FROM tickets GROUP BY DATE(created_at) ORDER BY date;
