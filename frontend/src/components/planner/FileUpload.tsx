"use client"

import { useState, ChangeEvent } from "react"
import { uploadImage } from "@/utils/api"
import { UploadResult } from "@/types/planner"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface Props {
	onResult: (data: UploadResult) => void
}

export default function FileUpload({ onResult }: Props) {
	const [file, setFile] = useState<File | null>(null)
	const [uploading, setUploading] = useState(false)

	const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
		if (e.target.files?.[0]) {
			setFile(e.target.files[0])
		}
	}

	const handleUpload = async () => {
		if (!file) return
		setUploading(true)
		try {
			const data = await uploadImage(file)
			onResult(data)
		} catch {
			alert("Upload failed")
		} finally {
			setUploading(false)
		}
	}

	return (
		<div className="flex flex-col gap-4 max-w-md mx-auto">
			<Input type="file" onChange={handleChange} />
			<Button onClick={handleUpload} disabled={uploading || !file}>
				{uploading ? "Analyzing..." : "Analyze Image"}
			</Button>
		</div>
	)
}
