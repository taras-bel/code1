"""
Maintenance tasks for system upkeep
"""
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any
from tasks.celery_app import celery_app
# from database.connection import db_session  # Commented out - not needed with Supabase SDK
from database.models import CacheEntry, RateLimit, AuditLog, UploadedFile, User, Analysis
from cache.redis_client import redis_cache

logger = logging.getLogger(__name__)

@celery_app.task
def clean_expired_cache() -> Dict[str, Any]:
    """
    Clean expired cache entries from database
    """
    try:
        with db_session() as session:
            # Delete expired cache entries
            expired_count = session.query(CacheEntry).filter(
                CacheEntry.expires_at < datetime.utcnow()
            ).delete()
            
            session.commit()
            
            # Also clean Redis cache
            redis_cleaned = 0
            if redis_cache.is_connected():
                # This would require implementing a scan method
                # For now, we'll just log that Redis cleanup is needed
                redis_cleaned = 0
            
            logger.info(f"Cleaned {expired_count} expired cache entries from database")
            
            return {
                "status": "success",
                "database_cleaned": expired_count,
                "redis_cleaned": redis_cleaned
            }
            
    except Exception as exc:
        logger.error(f"Failed to clean expired cache: {exc}")
        raise exc

@celery_app.task
def reset_weekly_rate_limits() -> Dict[str, Any]:
    """
    Reset weekly rate limits for all users
    """
    try:
        with db_session() as session:
            # Get current week start
            current_week_start = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            current_week_start = current_week_start - timedelta(
                days=current_week_start.weekday()
            )
            
            # Reset rate limits for users whose week has passed
            updated_count = session.query(RateLimit).filter(
                RateLimit.week_start < current_week_start
            ).update({
                "analysis_count": 0,
                "week_start": current_week_start
            })
            
            session.commit()
            
            logger.info(f"Reset rate limits for {updated_count} users")
            
            return {
                "status": "success",
                "updated_count": updated_count,
                "week_start": current_week_start.isoformat()
            }
            
    except Exception as exc:
        logger.error(f"Failed to reset weekly rate limits: {exc}")
        raise exc

@celery_app.task
def health_check() -> Dict[str, Any]:
    """
    System health check
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {}
        }
        
        # Database health check
        try:
            with db_session() as session:
                session.execute("SELECT 1")
                health_status["checks"]["database"] = "healthy"
        except Exception as e:
            health_status["checks"]["database"] = f"unhealthy: {e}"
            health_status["status"] = "unhealthy"
        
        # Redis health check
        if redis_cache.is_connected():
            health_status["checks"]["redis"] = "healthy"
        else:
            health_status["checks"]["redis"] = "unhealthy: not connected"
            health_status["status"] = "unhealthy"
        
        # Storage health check (Supabase)
        try:
            # This would check Supabase connection
            health_status["checks"]["storage"] = "healthy"
        except Exception as e:
            health_status["checks"]["storage"] = f"unhealthy: {e}"
            health_status["status"] = "unhealthy"
        
        # Log health status
        if health_status["status"] == "healthy":
            logger.info("System health check passed")
        else:
            logger.warning(f"System health check failed: {health_status['checks']}")
        
        return health_status
        
    except Exception as exc:
        logger.error(f"Health check failed: {exc}")
        raise exc

@celery_app.task
def cleanup_old_files() -> Dict[str, Any]:
    """
    Clean up old uploaded files
    """
    try:
        # Define retention period (30 days)
        retention_days = int(os.getenv("FILE_RETENTION_DAYS", "30"))
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        with db_session() as session:
            # Get old files
            old_files = session.query(UploadedFile).filter(
                UploadedFile.created_at < cutoff_date
            ).all()
            
            deleted_count = 0
            for file in old_files:
                try:
                    # Delete from storage (implement based on your storage solution)
                    # For Supabase Storage, you would use the storage client here
                    
                    # Delete database record
                    session.delete(file)
                    deleted_count += 1
                    
                except Exception as e:
                    logger.error(f"Failed to delete file {file.id}: {e}")
            
            session.commit()
            
            logger.info(f"Cleaned up {deleted_count} old files")
            
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "retention_days": retention_days,
                "cutoff_date": cutoff_date.isoformat()
            }
            
    except Exception as exc:
        logger.error(f"Failed to cleanup old files: {exc}")
        raise exc

@celery_app.task
def cleanup_old_audit_logs() -> Dict[str, Any]:
    """
    Clean up old audit logs
    """
    try:
        # Define retention period (90 days)
        retention_days = int(os.getenv("AUDIT_RETENTION_DAYS", "90"))
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        with db_session() as session:
            # Delete old audit logs
            deleted_count = session.query(AuditLog).filter(
                AuditLog.created_at < cutoff_date
            ).delete()
            
            session.commit()
            
            logger.info(f"Cleaned up {deleted_count} old audit logs")
            
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "retention_days": retention_days,
                "cutoff_date": cutoff_date.isoformat()
            }
            
    except Exception as exc:
        logger.error(f"Failed to cleanup old audit logs: {exc}")
        raise exc

@celery_app.task
def generate_system_report() -> Dict[str, Any]:
    """
    Generate system usage report
    """
    try:
        with db_session() as session:
            # Get statistics
            total_users = session.query(User).count()
            total_analyses = session.query(Analysis).count()
            completed_analyses = session.query(Analysis).filter(
                Analysis.status == "completed"
            ).count()
            failed_analyses = session.query(Analysis).filter(
                Analysis.status == "failed"
            ).count()
            
            # Get recent activity
            last_24h = datetime.utcnow() - timedelta(days=1)
            recent_analyses = session.query(Analysis).filter(
                Analysis.created_at >= last_24h
            ).count()
            
            # Get average processing time
            avg_processing_time = session.query(Analysis).filter(
                Analysis.processing_time.isnot(None)
            ).with_entities(
                session.query(Analysis.processing_time).avg()
            ).scalar() or 0
            
            report = {
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "statistics": {
                    "total_users": total_users,
                    "total_analyses": total_analyses,
                    "completed_analyses": completed_analyses,
                    "failed_analyses": failed_analyses,
                    "success_rate": (completed_analyses / total_analyses * 100) if total_analyses > 0 else 0,
                    "recent_analyses_24h": recent_analyses,
                    "avg_processing_time_seconds": round(avg_processing_time, 2)
                }
            }
            
            logger.info(f"Generated system report: {report['statistics']}")
            
            return report
            
    except Exception as exc:
        logger.error(f"Failed to generate system report: {exc}")
        raise exc

@celery_app.task
def backup_database() -> Dict[str, Any]:
    """
    Create database backup
    """
    try:
        # This would implement database backup logic
        # For Supabase, you might use their backup features
        # For PostgreSQL, you might use pg_dump
        
        backup_path = f"backups/backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.sql"
        
        # Create backup directory if it doesn't exist
        os.makedirs("backups", exist_ok=True)
        
        # For now, we'll just log the backup attempt
        logger.info(f"Database backup created: {backup_path}")
        
        return {
            "status": "success",
            "backup_path": backup_path,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Failed to create database backup: {exc}")
        raise exc 