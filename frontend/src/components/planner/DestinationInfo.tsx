"use client"

import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Destination } from "@/types/planner"
import { Button } from "@/components/ui/button"

interface Props {
	data: Destination
	onShowMore?: () => void
}

export default function DestinationInfo({ data, onShowMore }: Props) {
	return (
		<Card className="bg-white backdrop-blur border border-white/10 max-w-4xl mx-auto  rounded-2xl shadow-lg">
			<CardHeader>
				<CardTitle>Top Match: {data?.name}</CardTitle>
			</CardHeader>
			<CardContent className="text-sm space-y-2">
				<div className="flex flex-col space-y-2">
					{/* <p>
						<strong>Scene Type:</strong> {scene.toUpperCase()}
					</p> */}
					<p>
						<strong>Country:</strong> {data?.country}
					</p>
					<p>
						<strong>Best time to visit:</strong> {data?.bestSeason}
					</p>
					<p>
						<strong>Activities:</strong> {data?.activities.join(", ")}
					</p>
					<p>
						<strong>Description:</strong> <p className="text-muted-foreground">{data?.explanation}</p>
					</p>
				</div>
				{onShowMore && (
					<div className="mt-4">
						<Button onClick={onShowMore} variant="outline" className="text-sm font-medium">
							🔁 Show me more like this
						</Button>
					</div>
				)}
			</CardContent>
		</Card>
	)
}
