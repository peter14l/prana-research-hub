"""
Research Library router:
Foundational papers repository, searchable annotations, and user research notes.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from backend.database import get_db
from backend.models.models import ResearchDocument, ResearchNote, ResearchFinding
from backend.models.schemas import ResearchNoteCreate

router = APIRouter(prefix="/library", tags=["Research Library"])

@router.get("/documents")
def get_documents(
    query: Optional[str] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    q = db.query(ResearchDocument)
    if query:
        search_filter = f"%{query}%"
        q = q.filter(
            ResearchDocument.title.ilike(search_filter) |
            ResearchDocument.organisation.ilike(search_filter) |
            ResearchDocument.key_findings.ilike(search_filter) |
            ResearchDocument.tags.ilike(search_filter)
        )
    docs = q.order_by(ResearchDocument.id.asc()).all()

    results = []
    for d in docs:
        notes_count = len(d.notes)
        results.append({
            "id": d.id,
            "title": d.title,
            "organisation": d.organisation,
            "publication_date": d.publication_date,
            "geographic_coverage": d.geographic_coverage,
            "pollutants_studied": d.pollutants_studied,
            "methodology": d.methodology,
            "key_findings": d.key_findings,
            "limitations": d.limitations,
            "original_url": d.original_url,
            "study_type": d.study_type,
            "confidence_tier": d.confidence_tier,
            "tags": d.tags,
            "notes_count": notes_count
        })

    return results

@router.get("/notes")
def get_research_notes(
    document_id: Optional[int] = None,
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    q = db.query(ResearchNote)
    if document_id:
        q = q.filter_by(document_id=document_id)
    notes = q.order_by(ResearchNote.created_at.desc()).all()

    return [
        {
            "id": n.id,
            "document_id": n.document_id,
            "station_id": n.station_id,
            "title": n.title,
            "content": n.content,
            "tags": n.tags,
            "created_at": n.created_at.isoformat()
        }
        for n in notes
    ]

@router.post("/notes")
def create_research_note(
    note_in: ResearchNoteCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    note = ResearchNote(
        document_id=note_in.document_id,
        station_id=note_in.station_id,
        title=note_in.title,
        content=note_in.content,
        tags=note_in.tags,
        created_at=datetime.utcnow()
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "created_at": note.created_at.isoformat(),
        "status": "SUCCESS"
    }
