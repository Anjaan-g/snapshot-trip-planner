import { UploadResult } from "@/types/planner"

const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://localhost:5000"

export async function uploadImage(file: File): Promise<UploadResult> {
	const formData = new FormData()
	formData.append("file", file)

	const res = await fetch(`${API_BASE}/upload`, {
		method: "POST",
		body: formData,
	})

	if (!res.ok) {
		throw new Error("Upload failed")
	}

	const data: UploadResult = await res.json()
	return data
}

export async function getSimilarDestinations(scene_type: string): Promise<{ name: string; rank: number }[]> {
	const res = await fetch(`${API_BASE}/similar`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ scene_type }),
	})

	if (!res.ok) {
		throw new Error("Failed to fetch similar destinations")
	}

	const data = await res.json()
	return data
}

export async function getRandomDestination() {
	const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/random`)
	if (!res.ok) throw new Error("Random fetch failed")
	return res.json()
}
